"""Tests proxy support for DomainTools APIs"""

import pytest

from httpx import ConnectError
from tests.settings import api


class TestSsl:

    def test_account_information_using_proxy_with_custom_cert_should_succeed_if_using_the_valid_custom_cert(self):
        api.verify_ssl = "tests/e2e/mitmproxy-ca.pem"
        api.proxy_url = "http://localhost:8090"
        with api.account_information() as account_information:
            assert "products" in account_information
            for product in account_information:
                assert "id" in product
                assert "per_month_limit" in product
                assert "absolute_limit" in product
                assert "usage" in product
                assert "expiration_date" in product

    def test_account_information_using_proxy_with_custom_cert_should_be_successful_when_verify_ssl_is_disabled(self):
        api.verify_ssl = False
        api.proxy_url = "http://localhost:8090"
        with api.account_information() as account_information:
            assert "products" in account_information
            for product in account_information:
                assert "id" in product
                assert "per_month_limit" in product
                assert "absolute_limit" in product
                assert "usage" in product
                assert "expiration_date" in product

    def test_account_information_using_proxy_with_custom_cert_should_fail_when_verify_ssl_is_enabled_but_not_using_the_installed_custom_cert(
        self,
    ):
        api.verify_ssl = True
        api.proxy_url = "http://localhost:8090"
        with pytest.raises(ConnectError):
            account_information = api.account_information()
            account_information.response()
