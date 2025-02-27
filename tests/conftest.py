"""Configuration for test environment"""

import pytest


@pytest.fixture
def test_feeds_params():
    return {
        "sessionID": "test-session-id",
        "after": -60,
        "before": -120,
        "output_format": "csv",
        "endpoint": "download",
    }
