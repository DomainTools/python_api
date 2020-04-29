"""Adds async capabilities to the base product object"""
import asyncio
import aiohttp

from domaintools.base_results import Results

from domaintools.exceptions import ServiceUnavailableException, ServiceException

class _AIter(object):
    """A wrapper to wrap an AsyncResults as an async iterable"""
    __slots__ = ('results', 'iterator', )

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
    """The base (abstract) DomainTools' product definition with Async capabilities built in"""

    def __await__(self):
        return self.__awaitable__().__await__()

    async def _make_async_request(self, session):
        async with session.get(self.url, params=self.kwargs, **self.api.extra_aiohttp_params) as results:
            self.setStatus(results.status, results)
            if self.kwargs.get('format', 'json') == 'json':
                self._data = await results.json()
            else:
                self._data = await results.text()
            limit_exceeded, message = self.check_limit_exceeded()

            if limit_exceeded:
                self._limit_exceeded = True
                self._limit_exceeded_message = message

    async def __awaitable__(self):
        if self._data is None:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=self.api.verify_ssl)) as session:
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
