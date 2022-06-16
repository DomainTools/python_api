"""Tests async interaction support for DomainTools APIs"""
import asyncio

from tests.settings import api, vcr


def run_async(future):
    return asyncio.get_event_loop().run_until_complete(future)


@vcr.use_cassette
def test_async_iteration():
    async def async_iter_test():
        domains = []
        async for domain in api.domain_search('google'):
            domains += domain
        return domains

    domains = run_async(async_iter_test())
    assert domains
    for domain in domains:
        assert type(domain) == str


@vcr.use_cassette
def test_async_context_manager():
    async def async_context_manager_test():
        async with api.domain_search('google') as results:
            return results

    results = run_async(async_context_manager_test())
    assert results


@vcr.use_cassette
def test_async_simple_await():
    async def simple_await():
        results = await api.domain_search('google')
        return results

    results = run_async(simple_await())
    assert results


@vcr.use_cassette
def test_async_simple_await_post():
    async def simple_await():
        results = await api.iris_investigate(domains=['amazon.com', 'google.com'])
        return results

    investigation_results = run_async(simple_await())
    assert investigation_results['results_count']
    for result in investigation_results:
        assert result['domain'] in ['amazon.com', 'google.com']


@vcr.use_cassette
def test_async_simple_await_patch():
    async def simple_await():
        results = await api.iris_detect_manage_watchlist_domains(watchlist_domain_ids=["gae08rdVWG"], state="watched")
        return results

    detect_results = run_async(simple_await())
    assert detect_results['watchlist_domains'][0]['state'] == "watched"