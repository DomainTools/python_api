"""Defines the used Result object based on the current versions and/or features available to Python runtime

Additionally, defines any custom result objects that may be used to enable more Pythonic interaction with endpoints.
"""

import logging
import httpx
import time

try:  # pragma: no cover
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from ordereddict import OrderedDict

from itertools import zip_longest, chain
from typing import Generator

from domaintools_async import AsyncResults as Results


log = logging.getLogger(__name__)


class Reputation(Results):
    """Returns the reputation results in a format that can quickly be converted into floats / ints"""

    def __float__(self):
        return float(self["risk_score"])

    def __int__(self):
        return int(self["risk_score"])


class GroupedIterable(Results):
    """Returns a results item in a format that allows for grouped iteration of mulpitle result lists"""

    def _items(self):
        if self._items_list is None:
            self._items_list = chain(
                *[
                    zip_longest([], value, fillvalue=key)
                    for key, value in self.response().items()
                    if type(value) in (list, tuple)
                ]
            )

        return self._items_list


class ParsedWhois(Results):
    """Returns the parsed whois results in a format that can quickly be flattened"""

    def flattened(self):
        """Returns a flattened version of the parsed whois data"""
        parsed = self["parsed_whois"]
        flat = OrderedDict()
        for key in (
            "domain",
            "created_date",
            "updated_date",
            "expired_date",
            "statuses",
            "name_servers",
        ):
            if key in parsed:
                value = parsed[key]
                flat[key] = " | ".join(value) if type(value) in (list, tuple) else value

        registrar = parsed.get("registrar", {})
        for key in (
            "name",
            "abuse_contact_phone",
            "abuse_contact_email",
            "iana_id",
            "url",
            "whois_server",
        ):
            if key in registrar:
                flat["registrar_{0}".format(key)] = registrar[key]

        if "networks" in parsed:
            networks = parsed.get("networks")
            for network in networks:
                id = network.get("id")
                for key in (
                    "range",
                    "asn",
                    "org",
                    "parent",
                    "customer",
                    "country",
                    "phone",
                    "status",
                    "source",
                    "updated_date",
                    "created_date",
                ):
                    if key in network:
                        value = network[key]
                        flat["network_{0}".format(id)] = (
                            " ".join(value) if type(value) in (list, tuple) else value
                        )

        if "contacts" in parsed:
            contacts = parsed.get("contacts")
            if type(contacts) is list:
                # handle IP-style contacts, which show up as a list
                for contact in contacts:
                    contact_type = contact.get("type")
                    for key in (
                        "name",
                        "email",
                        "org",
                        "abuse_mailbos",
                        "address",
                        "street",
                        "city",
                        "state",
                        "postal",
                        "country",
                        "phone",
                        "fax",
                    ):
                        if key in contact:
                            value = contact[key]
                            flat["{0}_{1}".format(contact_type, key)] = (
                                " ".join(value) if type(value) in (list, tuple) else value
                            )

            elif type(contacts) is dict:
                for contact_type in ("registrant", "admin", "tech", "billing"):
                    contact = contacts.get(contact_type, {})
                    for key in (
                        "name",
                        "email",
                        "org",
                        "street",
                        "city",
                        "state",
                        "postal",
                        "country",
                        "phone",
                        "fax",
                    ):
                        if key in contact:
                            value = contact[key]
                            flat["{0}_{1}".format(contact_type, key)] = (
                                " ".join(value) if type(value) in (list, tuple) else value
                            )

        return flat


class ParsedDomainRdap(Results):
    """Returns the parsed domain rdap results in a format that can quickly be flattened"""

    def flattened(self):
        """Returns a flattened version of the parsed domain rdap data"""
        parsed = self["parsed_domain_rdap"]
        flat = OrderedDict()
        for key in (
            "domain",
            "handle",
            "domain_statuses",
            "creation_date",
            "last_changed_date",
            "expiration_date",
            "dnssec",
            "nameservers",
            "conformance",
            "emails",
            "email_domains",
            "unclassified_emails",
        ):
            if key in parsed:
                value = parsed[key]
                flat[key] = " | ".join(value) if type(value) in (list, tuple) else value

        registrar = parsed.get("registrar", {})
        for registrar_key, registrar_value in registrar.items():
            if registrar_key == "contacts":
                for i, contact in enumerate(registrar_value, start=1):
                    for contact_key, contact_value in contact.items():
                        flat[f"registrar_contacts_{contact_key}"] = (
                            " | ".join(contact_value)
                            if type(contact_value) in (list, tuple)
                            else contact_value
                        )

                continue
            flat[f"registrar_{registrar_key}"] = registrar_value

        contacts = parsed.get("contacts")
        if contacts:
            for i, contact in enumerate(contacts, start=1):
                for contact_key, contact_value in contact.items():
                    flat[f"contact_{contact_key}_{i}"] = (
                        " | ".join(contact_value) if type(contact_value) in (list, tuple) else contact_value
                    )

        return flat


class FeedsResults(Results):
    """
    Real Time Threat Feeds (RTTF) returns an application/ndjson stream.
    With this we use httpx stream to process each JSON object efficiently.

    Highlevel process:

    httpx stream -> check status code -> yield back data to client -> repeat if 206

    Returns the generator object for feeds results.
    """

    latest_feeds_status_code = None

    def _make_request(self) -> Generator:
        """
        Creates and manages the httpx stream request, yielding data line by line.
        This is the core generator that communicates with the DT frontend API server.
        """
        session_info = self._get_session_params_and_headers()
        headers = session_info.get("headers")
        parameters = session_info.get("parameters")

        try:
            with httpx.stream(
                "GET",
                self.url,
                headers=headers,
                params=parameters,
                verify=self.api.verify_ssl,
                proxy=self.api.proxy_url,
                timeout=None,
            ) as response:
                self.latest_feeds_status_code = response.status_code
                # assigned the status code to `latest_feeds_status_code`
                # started the process
                yield {"status_ready": True}

                for line in response.iter_lines():
                    yield line
        except Exception as e:
            self.latest_feeds_status_code = 500
            raise e

    def _get_results(self) -> Generator:
        try:
            feeds_generator = self._make_request()
            next(feeds_generator)  # to start the generator process
            self.setStatus(self.latest_feeds_status_code)  # set the status already

            # yield the rest of the feeds
            yield from feeds_generator
        except Exception as e:
            self.setStatus(500, reason_text=e)
            return

    def data(self) -> Generator:
        self._data = self._get_results()
        return self._data

    def response(self) -> Generator:
        status_code = None
        while status_code != 200:
            try:
                feed_response_generator = self.data()

                yield from feed_response_generator
                status_code = self.status
                self._data = None  # clear the data here

                if not self.kwargs.get("sessionID"):
                    # we'll only do iterative request for queries that has sessionID.
                    # Otherwise, we will have an infinite request if sessionID was not provided but the required data asked is more than the maximum (1 hour of data)
                    break
            except Exception as e:
                self.setStatus(500, reason_text=e)
                break  # safely close the while loop if there's any error above

    def __str__(self):
        return f"{self.__class__.__name__} - {self.product}"
