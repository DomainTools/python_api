"""Tests async interaction support for DomainTools APIs"""

import asyncio
import pytest

from tests.settings import api, vcr


@vcr.use_cassette
@pytest.mark.asyncio
async def test_async_iteration():
    results = await api.domain_search("google")
    assert results

    list_of_domains = []
    for domain in results:
        list_of_domains += domain

    for domain in list_of_domains:
        assert type(domain) == str


@vcr.use_cassette
@pytest.mark.asyncio
async def test_async_context_manager():
    results = await api.domain_search("google")
    assert results


@vcr.use_cassette
@pytest.mark.asyncio
async def test_async_simple_await():
    results = await api.domain_search("google")
    assert results


@vcr.use_cassette
@pytest.mark.asyncio
async def test_async_simple_await_post():
    investigation_results = await api.iris_investigate(domains=["amazon.com", "google.com"])
    assert investigation_results["results_count"]
    for result in investigation_results:
        assert result["domain"] in ["amazon.com", "google.com"]


@vcr.use_cassette
@pytest.mark.asyncio
async def test_async_simple_await_patch():
    detect_results = await api.iris_detect_manage_watchlist_domains(watchlist_domain_ids=["gae08rdVWG"], state="watched")
    assert detect_results["watchlist_domains"][0]["state"] == "watched"
