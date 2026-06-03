"""Tests async interaction support for DomainTools APIs"""

import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

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


@pytest.mark.asyncio
async def test_async_irisql_uses_raw_body():
    query = "# IrisQL-1.0\nDOMAIN CONTAINS \"phishing\""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": {"results": [], "results_count": 0}}

    with patch("domaintools_async.AsyncClient") as mock_client:
        mock_session = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_session
        mock_session.post.return_value = mock_response

        result = await api.iris_investigate(irisql=query)

        _, kwargs = mock_session.post.call_args
        assert kwargs.get("content") == query
        assert "data" not in kwargs
        assert kwargs.get("headers", {}).get("Content-Type") == "text/plain"


@pytest.mark.asyncio
async def test_async_irisql_with_pagination_kwargs():
    query = "# IrisQL-1.0\nDOMAIN CONTAINS \"phishing\""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": {"results": [], "results_count": 0}}

    with patch("domaintools_async.AsyncClient") as mock_client:
        mock_session = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_session
        mock_session.post.return_value = mock_response

        result = await api.iris_investigate(irisql=query, page_size=50, sort_by="risk_score")

        _, kwargs = mock_session.post.call_args
        assert kwargs.get("content") == query
        assert "page_size" in kwargs.get("params", {})
        assert "sort_by" in kwargs.get("params", {})
