"""Test that iris_enrich only triggers account_information once per API instance."""

from unittest.mock import patch, MagicMock

from domaintools import API
from domaintools.exceptions import ServiceUnavailableException


def test_iris_enrich_does_not_repeat_account_info_call():
    """Confirm account_information is fetched only once for multiple iris_enrich calls on same API instance."""
    # Reset class-level state that may have been set by previous tests
    API.limits = {}
    API.limits_set = False

    api = API("test_user", "test_key", rate_limit=True)

    # Fake account info response
    fake_account_data = {
        "response": {
            "products": [
                {"id": "iris-enrich", "per_minute_limit": 10, "per_hour_limit": 100}
            ]
        }
    }

    # Fake iris-enrich response
    fake_enrich_data = {
        "response": {
            "results": [{"domain": "google.com"}],
            "results_count": 1,
            "missing_domains": [],
            "limit_exceeded": False,
        }
    }

    call_log = []

    with patch("domaintools.base_results.Client") as mock_client:
        mock_session = MagicMock()
        mock_client.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_client.return_value.__exit__ = MagicMock(return_value=False)

        def fake_get(url, **kwargs):
            call_log.append(("GET", url))
            resp = MagicMock()
            resp.status_code = 200
            if "/v1/account" in url:
                resp.json.return_value = fake_account_data
            return resp

        def fake_post(url, **kwargs):
            call_log.append(("POST", url))
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = fake_enrich_data
            return resp

        mock_session.get.side_effect = fake_get
        mock_session.post.side_effect = fake_post

        # First call - should trigger account_information (GET /v1/account)
        api.iris_enrich("google.com")
        # Second call - should NOT trigger account_information again
        api.iris_enrich("amazon.com")

    # Count how many times /v1/account was called
    account_calls = [c for c in call_log if "/v1/account" in c[1]]
    enrich_calls = [c for c in call_log if "/v1/iris-enrich" in c[1]]

    assert len(account_calls) == 1, (
        f"Expected exactly 1 account_information call, got {len(account_calls)}. "
        f"Full call log: {call_log}"
    )
    assert len(enrich_calls) == 2, (
        f"Expected exactly 2 iris_enrich calls, got {len(enrich_calls)}. "
        f"Full call log: {call_log}"
    )


def test_iris_enrich_succeeds_when_account_info_is_rate_limited():
    """Verify that iris_enrich proceeds normally even if account_information returns a 503."""
    # Reset class-level state that may have been set by previous tests
    API.limits = {}
    API.limits_set = False

    api = API("test_user", "test_key", rate_limit=True)

    # Fake iris-enrich response
    fake_enrich_data = {
        "response": {
            "results": [{"domain": "google.com"}],
            "results_count": 1,
            "missing_domains": [],
            "limit_exceeded": False,
        }
    }

    call_log = []

    with patch("domaintools.base_results.Client") as mock_client, \
         patch("domaintools.base_results.time.sleep"):
        mock_session = MagicMock()
        mock_client.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_client.return_value.__exit__ = MagicMock(return_value=False)

        def fake_get(url, **kwargs):
            call_log.append(("GET", url))
            resp = MagicMock()
            if "/v1/account" in url:
                # Simulate a 503 rate limit on account_information
                resp.status_code = 503
                resp.json.return_value = {"error": {"message": "Rate limit exceeded"}}
            else:
                resp.status_code = 200
                resp.json.return_value = {}
            return resp

        def fake_post(url, **kwargs):
            call_log.append(("POST", url))
            resp = MagicMock()
            resp.status_code = 200
            resp.json.return_value = fake_enrich_data
            return resp

        mock_session.get.side_effect = fake_get
        mock_session.post.side_effect = fake_post

        # This should NOT raise an exception despite account_info returning 503
        result = api.iris_enrich("google.com")

    # Verify the iris_enrich call succeeded
    enrich_calls = [c for c in call_log if "/v1/iris-enrich" in c[1]]
    assert len(enrich_calls) == 1, (
        f"Expected 1 iris_enrich call, got {len(enrich_calls)}. Full call log: {call_log}"
    )

    # Verify limits_set was set to True so it won't retry account_info
    assert api.limits_set is True

    # Verify the result contains expected data
    assert result["results_count"] == 1
    assert result["results"][0]["domain"] == "google.com"
