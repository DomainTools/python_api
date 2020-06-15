"""Defines the base result object - which specifies how DomainTools' API endpoints will be interacted with"""
import collections
import json
import re
import time
import logging
from datetime import datetime

from domaintools.exceptions import (BadRequestException, InternalServerErrorException, NotAuthorizedException,
                                    NotFoundException, ServiceException, ServiceUnavailableException,
                                    IncompleteResponseException, RequestUriTooLongException)
from requests import Session

try: # pragma: no cover
    from collections.abc import MutableMapping, MutableSequence
except ImportError: # pragma: no cover
    from collections import MutableMapping, MutableSequence

log = logging.getLogger(__name__)

class Results(MutableMapping, MutableSequence):
    """The base (abstract) DomainTools result definition"""

    def __init__(self, api, product, url, items_path=(), response_path=('response', ), proxy_url=None, **kwargs):
        self.api = api
        self.product = product
        self.url = url
        self.proxy_url = proxy_url
        self.items_path = items_path
        self.response_path = response_path
        self.kwargs = kwargs
        self._response = None
        self._items_list = None
        self._data = None
        self._limit_exceeded = None
        self._limit_exceeded_message = None

    def _wait_time(self):
        if not self.api.rate_limit or not self.product in self.api.limits:
            return 0

        now = datetime.now()
        limit = self.api.limits[self.product]
        if 'last_scheduled' not in limit:
            limit['last_scheduled'] = now
            return None

        safe_after = limit['last_scheduled'] + limit['interval']
        wait_for = 0
        if now < safe_after:
            wait_for = safe_after - now
            wait_for = float(wait_for.seconds) + (float(wait_for.microseconds) / 1000000.0)
            limit['last_scheduled'] = safe_after
        else:
            limit['last_scheduled'] = now

        return wait_for

    def _make_request(self):
        with Session() as session:
            session.proxies = self.api.extra_request_params.get('proxies', None)
            if self.product in ['iris-investigate']:
                post_data = self.kwargs.copy()
                post_data.update(self.api.extra_request_params)
                return session.post(url=self.url, verify=self.api.verify_ssl,
                        data=post_data)
            else:
                return session.get(url=self.url, params=self.kwargs, verify=self.api.verify_ssl,
                        **self.api.extra_request_params)

    def _get_results(self):
        wait_for = self._wait_time()
        if self.api.rate_limit and (wait_for is None or self.product == 'account-information'):
            data = self._make_request()
            if data.status_code == 503: # pragma: no cover
                sleeptime = 60
                log.info('503 encountered for [%s] - sleeping [%s] seconds before retrying request.',
                         self.product, sleeptime)
                time.sleep(sleeptime)
                self._wait_time()
                data = self._make_request()
            return data

        if wait_for > 0:
            log.info('Sleeping for [%s] prior to requesting [%s].',
                     wait_for, self.product)
            time.sleep(wait_for)
        return self._make_request()

    def data(self):
        if self._data is None:
            results = self._get_results()
            self.setStatus(results.status_code, results)
            if self.kwargs.get('format', 'json') == 'json':
                self._data = results.json()
            else:
                self._data = results.text
            limit_exceeded, message = self.check_limit_exceeded()

            if limit_exceeded:
                self._limit_exceeded = True
                self._limit_exceeded_message = message

        if self._limit_exceeded is True:
            raise ServiceException(503, "Limit Exceeded{}".format(self._limit_exceeded_message))
        else:
            return self._data

    def check_limit_exceeded(self):
        if self.kwargs.get('format', 'json') == 'json':
            if ("response" in self._data and
                "limit_exceeded" in self._data['response'] and
                self._data['response']['limit_exceeded'] is True):
                return True, self._data['response']['message']
        else:
            # TODO: handle html, xml response errors better.
            if "response" in self._data and "limit_exdeeded" in self._data:
                return True, "limit exceeded"
        return False, ""

    @property
    def status(self):
        if not getattr(self, '_status', None):
            self._status = self._get_results().status_code

        return self._status

    def setStatus(self, code, response=None):
        self._status = code
        if code == 200:
            return

        reason = None
        if response is not None:
            try:
                reason = response.json()
            except Exception: # pragma: no cover
                reason = response.text
                if callable(reason):
                    reason = reason()

        if code == 400:
            raise BadRequestException(code, reason)
        elif code == 403:
            raise NotAuthorizedException(code, reason)
        elif code == 404:
            raise NotFoundException(code, reason)
        elif code == 500: # pragma: no cover
            raise InternalServerErrorException(code, reason)
        elif code == 503: # pragma: no cover
            raise ServiceUnavailableException(code, reason)
        elif code == 206: # pragma: no cover
            raise IncompleteResponseException(code, reason)
        elif code == 414: # pragma: no cover
            raise RequestUriTooLongException(code, reason)
        else: # pragma: no cover
            raise ServiceException(code, 'Unknown Exception')

    def response(self):
        if self._response is None:
            response = self.data()
            for step in self.response_path:
                response = response[step]
            self._response = response

        return self._response

    def items(self):
        return self.response().items()

    def emails(self):
        """Find and returns all emails mentioned in the response"""
        return set(re.findall(r'[\w\.-]+@[\w\.-]+', str(self.response())))

    def _items(self):
        if self._items_list is None:
            if not self.items_path:
                return self.items()

            response = self.response()
            for step in self.items_path:
                response = response[step]
            self._items_list = response

        return self._items_list

    def __getitem__(self, key):
        return self.response()[key]

    def __setitem__(self, key, item):
        self.response()[key] = item

    def __delitem__(self, key):
        del self.response()[key]

    def __iter__(self):
        return self._items().__iter__()

    def has_key(self, key):
        return key in self.response()

    def values(self):
        return self.response().values()

    def insert(self, index, item):
        return self._items().insert(index, item)

    def update(self, *args, **kwargs):
        return self.response().update(*args, **kwargs)

    def __len__(self):
        return len(self._items())

    def __enter__(self):
        self.data()
        return self

    def __exit__(self, *args):
        return

    @property
    def json(self):
        self.kwargs.pop('format', None)
        return self.__class__(format='json', product=self.product, url=self.url, items_path=self.items_path,
                              response_path=self.response_path, api=self.api, **self.kwargs)

    @property
    def xml(self):
        self.kwargs.pop('format', None)
        return self.__class__(format='xml', product=self.product, url=self.url, items_path=self.items_path,
                              response_path=self.response_path, api=self.api, **self.kwargs)

    @property
    def html(self):
        self.kwargs.pop('format', None)
        return self.__class__(api=self.api, product=self.product, url=self.url, items_path=self.items_path,
                              response_path=self.response_path, format='html', **self.kwargs)

    def as_list(self):
        return '\n'.join([json.dumps(item, indent=4, separators=(',', ': ')) for item in self._items()])

    def __str__(self):
        return str(json.dumps(self.data(), indent=4,
                              separators=(',', ': ')) if self.kwargs.get('format', 'json') == 'json' else self.data())
