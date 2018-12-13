"""Defines the used Result object based on the current versions and/or features available to Python runtime

Additionally, defines any custom result objects that may be used to enable more Pythonic interaction with endpoints.
"""
import sys
from itertools import chain

major, minor, patch = sys.version_info[:3]

try: # pragma: no cover
    from collections import OrderedDict
except ImportError: # pragma: no cover
    from ordereddict import OrderedDict

if major >= 3: # pragma: no cover
    from itertools import zip_longest
else: # pragma: no cover
    from itertools import izip_longest as zip_longest

if major >= 3 and (minor > 5 or (minor == 5 and patch >= 3)):
    from domaintools_async import AsyncResults as Results
else: # pragma: no cover
    from domaintools.base_results import Results


class Reputation(Results):
    """Returns the reputation results in a format that can quickly be converted into floats / ints"""

    def __float__(self):
        return float(self['risk_score'])

    def __int__(self):
        return int(self['risk_score'])


class GroupedIterable(Results):
    """Returns a results item in a format that allows for grouped iteration of mulpitle result lists"""

    def _items(self):
        if self._items_list is None:
            self._items_list = chain(*[zip_longest([], value, fillvalue=key) for key, value in self.response().items()
                                       if type(value) in (list, tuple)])

        return self._items_list


class ParsedWhois(Results):
    """Returns the parsed whois results in a format that can quickly be flattened"""

    def flattened(self):
        """Returns a flattened version of the parsed whois data"""
        parsed = self['parsed_whois']
        flat = OrderedDict()
        for key in ('domain', 'created_date', 'updated_date', 'expired_date', 'statuses', 'name_servers'):
            value = parsed[key]
            flat[key] = ' | '.join(value) if type(value) in (list, tuple) else value

        registrar = parsed.get('registrar', {})
        for key in ('name', 'abuse_contact_phone', 'abuse_contact_email', 'iana_id', 'url', 'whois_server'):
            flat['registrar_{0}'.format(key)] = registrar[key]

        for contact_type in ('registrant', 'admin', 'tech', 'billing'):
            contact = parsed.get('contacts', {}).get(contact_type, {})
            for key in ('name', 'email', 'org', 'street', 'city', 'state', 'postal', 'country', 'phone', 'fax'):
                value = contact[key]
                flat['{0}_{1}'.format(contact_type, key)] = ' '.join(value) if type(value) in (list, tuple) else value

        return flat
