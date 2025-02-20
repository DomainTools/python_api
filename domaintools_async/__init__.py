"""Adds async capabilities to the base product object"""

import asyncio

from copy import deepcopy
from httpx import AsyncClient

from domaintools.base_results import Results
from domaintools.constants import FEEDS_PRODUCTS_LIST, OutputFormat, HEADER_ACCEPT_KEY_CSV_FORMAT
from domaintools.exceptions import ServiceUnavailableException


class _AIter(object):
    """A wrapper to wrap an AsyncResults as an async iterable"""

    __slots__ = (
        "results",
        "iterator",
    )

    def __init__(self, results):
        self.results = results
        self.iterator = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.iterator is None:
            await self.results
            self.iterator = self.results._items().__iter__()

        try:
            return self.iterator.__next__()
        except StopIteration:
            raise StopAsyncIteration


class AsyncResults(Results):
    """The base (abstract) DomainTools product definition with Async capabilities built in"""

    def __await__(self):
        return self.__awaitable__().__await__()

    async def _make_async_request(self, session):
        if self.product in ["iris-investigate", "iris-enrich", "iris-detect-escalate-domains"]:
            post_data = self.kwargs.copy()
            post_data.update(self.api.extra_request_params)
            results = await session.post(url=self.url, data=post_data)
        elif self.product in ["iris-detect-manage-watchlist-domains"]:
            patch_data = self.kwargs.copy()
            patch_data.update(self.api.extra_request_params)
            results = await session.patch(url=self.url, json=patch_data)
        elif self.product in FEEDS_PRODUCTS_LIST:
            session_params = self._get_session_params()
            parameters = session_params.get("parameters")
            headers = session_params.get("headers")
            results = await session.get(url=self.url, params=parameters, headers=headers, **self.api.extra_request_params)
        else:
            results = await session.get(url=self.url, params=self.kwargs, **self.api.extra_request_params)
        if results:
            self.setStatus(results.status_code, results)
            if self.kwargs.get("format", "json") == "json":
                self._data = results.json()
            else:
                self._data = results.text()

            self.check_limit_exceeded()

    async def __awaitable__(self):
        if self._data is None:

            async with AsyncClient(verify=self.api.verify_ssl, proxy=self.api.proxy_url, timeout=None) as session:
                wait_time = self._wait_time()
                if wait_time is None and self.api:
                    try:
                        await self._make_async_request(session)
                    except ServiceUnavailableException:
                        await asyncio.sleep(60)
                        self._wait_time()
                        await self._make_async_request(session)
                else:
                    await asyncio.sleep(wait_time)
                    await self._make_async_request(session)

        return self

    def __aiter__(self):
        return _AIter(self)

    async def __aenter__(self):
        return await self

    async def __aexit__(self, *args):
        return
