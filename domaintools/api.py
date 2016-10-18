from datetime import datetime, timedelta
from hashlib import sha1
from hmac import new as hmac
from types import MethodType

import requests

from domaintools.results import GroupedIterable, ParsedWhois, Reputation, Results


def delimited(items, character='|'):
    """Returns a character delimited version of the provided list as a Python string"""
    return '|'.join(items) if type(items) in (list, tuple, set) else items


class API(object):
    """Enables interacting with the DomainTool's API via Python:

           from domaintools import API

           api = API('my_name', 'my_key')
           results = api.domain_search('domain')

        By default the API will automatically space out your requests to match your rate limits.
        If your running over multiple Python runtimes, have your own rate limiting approach, or are doing a one-off
        query (such as for a CLI command) you can set rate_limit=False to turn this feature off.

        If you encounter SSL errors you can pass in verify_ssl=False to avoid verification of the SSL cert.
        To use the API without SSL in it's entirety pass in https=False.

       For detailed usage information of all API calls see: https://www.domaintools.com/resources/api-documentation/
    """
    limits = {}

    def __init__(self, username, key, https=True, verify_ssl=True, rate_limit=True, **default_parameters):
        self.username = username
        self.key = key
        self.default_parameters = default_parameters
        self.https = https
        self.verify_ssl = verify_ssl
        self.rate_limit = rate_limit
        if rate_limit and not self.limits:
            for product in self.account_information():
                self.limits[product['id']] = {'interval': timedelta(seconds=60 / float(product['per_minute_limit']))}

    def _results(self, product, path, cls=Results, **kwargs):
        """Returns _results for the specified API path with the specified **kwargs parameters"""
        uri = '/'.join(('{0}://api.domaintools.com'.format('https' if self.https else 'http'), path.lstrip('/')))
        parameters = self.default_parameters.copy()
        parameters['api_username'] = self.username
        parameters['api_key'] = self.key
        if not self.https:
            parameters['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            parameters['signature'] = hmac(self.key.encode('utf8'), ''.join([self.username, parameters['timestamp'],
                                                                             path]).encode('utf8'),
                                           digestmod=sha1).hexdigest()
        parameters.update(dict((key, str(value).lower() if value in (True, False) else value) for
                               key, value in kwargs.items() if value is not None))
        return cls(self, product, uri, **parameters)

    def account_information(self, **kwargs):
        """Provides a snapshot of your accounts current API usage"""
        return self._results('account-information', '/v1/account', items_path=('products', ), **kwargs)

    def brand_monitor(self, query, exclude=[], domain_status=None, days_back=None, **kwargs):
        """Pass in one or more terms as a list or separated by the pipe character ( | )"""
        return self._results('mark-alert', '/v1/mark-alert', query=delimited(query), exclude=delimited(exclude),
                            domain_status=domain_status, days_back=days_back, items_path=('alerts', ), **kwargs)

    def domain_profile(self, query, **kwargs):
        """Returns a profile for the specified domain name"""
        return self._results('domain-profile', '/v1/{0}'.format(query))

    def domain_search(self, query, exclude_query=[], max_length=25, min_length=1, has_hyphen=True, has_number=True,
                      active_only=False, deleted_only=False, anchor_left=False, anchor_right=False, page=1, **kwargs):
        """Each term in the query string must be at least three characters long.
           Pass in a list or use spaces to separate multiple terms.
        """
        return self._results('domain-search', '/v2/domain-search', query=delimited(query, ' '),
                            exclude_query=delimited(exclude_query, ' '),
                            max_length=max_length, min_length=min_length, has_hyphen=has_hyphen, has_number=has_number,
                            active_only=active_only, deleted_only=deleted_only, anchor_left=anchor_left,
                            anchor_right=anchor_right, page=page, items_path=('results', ), **kwargs)

    def domain_suggestions(self, query, **kwargs):
        """Passed in name must be at least two characters long. Use a list or spaces to separate multiple terms."""
        return self._results('domain-suggestions', '/v1/domain-suggestions', query=delimited(query, ' '),
                            items_path=('suggestions', ), **kwargs)

    def hosting_history(self, query, **kwargs):
        """Returns the hosting history from the given domain name"""
        return self._results('hosting-history', '/v1/{0}/hosting-history'.format(query), cls=GroupedIterable, **kwargs)

    def ip_monitor(self, query, days_back=0, page=1, **kwargs):
        """Pass in the IP Address you wish to query ( i.e. 199.30.228.112 )."""
        return self._results('ip-monitor', '/v1/ip-monitor', query=query, days_back=days_back, page=page,
                            items_path=('alerts', ), **kwargs)

    def ip_registrant_monitor(self, query, days_back=0, search_type="all", server=None, country=None, org=None, page=1,
                              include_total_count=False, **kwargs):
        """Query based on free text query terms"""
        return self._results('ip-registrant-monitor', '/v1/ip-registrant-monitor', query=query,
                            days_back=days_back, search_type=search_type, server=server, country=country, org=org,
                            page=page, include_total_count=include_total_count, **kwargs)

    def name_server_monitor(self, query, days_back=0, page=1, **kwargs):
        """Pass in the hostname of the Name Server you wish to query ( i.e. dynect.net )."""
        return self._results('name-server-monitor', '/v1/name-server-monitor', query=query, days_back=days_back,
                            page=page, items_path=('alerts', ), **kwargs)

    def parsed_whois(self, query, **kwargs):
        """Pass in a domain name"""
        return self._results('parsed-whois', '/v1/{0}/whois/parsed'.format(query), cls=ParsedWhois, **kwargs)

    def registrant_monitor(self, query, exclude=[], days_back=0, limit=None, **kwargs):
        """One or more terms as a Python list or separated by the pipe character ( | )."""
        return self._results('registrant-alert', '/v1/registrant-alert', query=delimited(query),
                            exclude=delimited(exclude), days_back=days_back, limit=limit, items_path=('alerts', ),
                            **kwargs)

    def reputation(self, query, include_reasons=False, **kwargs):
        """Pass in a domain name to see its reputation score"""
        return self._results('reputation', '/v1/reputation', domain=query, include_reasons=include_reasons,
                            cls=Reputation, **kwargs)

    def reverse_ip(self, domain=None, limit=None, **kwargs):
        """Pass in a domain name."""
        return self._results('reverse-ip', '/v1/{0}/reverse-ip'.format(domain), limit=limit, **kwargs)

    def host_domains(self, ip=None, limit=None, **kwargs):
        """Pass in an IP address."""
        return self._results('reverse-ip', '/v1/{0}/host-domains'.format(ip), limit=limit, **kwargs)

    def reverse_ip_whois(self, query=None, ip=None, country=None, server=None, include_total_count=False, page=1,
                         **kwargs):
        """Pass in an IP address or a list of free text query terms."""
        if (ip and query) or not (ip or query):
            raise ValueError('Query or IP Address (but not both) must be defined')

        return self._results('reverse-ip-whois', '/v1/reverse-ip-whois', query=query, ip=ip, country=country,
                            server=server, include_total_count=include_total_count, page=page, items_path=('records', ),
                            **kwargs)

    def reverse_name_server(self, query, limit=None, **kwargs):
        """Pass in a domain name or a name server."""
        return self._results('reverse-name-server', '/v1/{0}/name-server-domains'.format(query),
                            items_path=('primary_domains', ), limit=limit, **kwargs)

    def reverse_whois(self, query, exclude=[], scope='current', mode=None, **kwargs):
        """List of one or more terms to search for in the Whois record,
           as a Python list or separated with the pipe character ( | ).
        """
        return self._results('reverse-whois', '/v1/reverse-whois', terms=delimited(query), exclude=delimited(exclude),
                            scope=scope, mode=mode, **kwargs)

    def whois(self, query, **kwargs):
        """Pass in a domain name or an IP address to perform a whois lookup."""
        return self._results('whois', '/v1/{0}/whois'.format(query), **kwargs)

    def whois_history(self, query, **kwargs):
        """Pass in a domain name."""
        return self._results('whois-history', '/v1/{0}/whois/history'.format(query), items_path=('history', ), **kwargs)
