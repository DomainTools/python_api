"""Adds async capabilities to the base product object"""
import asyncio
import aiohttp

from domaintools.base_results import Results


class AIter(object):
    """A wrapper to turn non async-iterators into async compatible iterators"""
    __slots__ = ('iterator', )

    def __init__(self, iterator):
        self.iterator = iterator

    def __aiter__(self):
        return self

    async def __anext__(self):
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

    async def __awaitable__(self):
        if self._data is None:
            with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=self.api.verify_ssl)) as session:
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

    async def __aiter__(self):
        await self
        return AIter(self._items().__iter__())

    async def __aenter__(self):
        return await self

    async def __aexit__(self, *args):
        return
