"""Tests proxy support for DomainTools APIs"""

import pytest

from httpx import ProxyError
from tests.settings import api


class TestProxy:

    def test_account_information_using_proxy_with_basic_auth_should_succeed_if_correct_username_and_password_were_used(self):
        api.verify_ssl = False
        api.proxy_url = "http://username:pass@localhost:8080"
        with api.account_information() as account_information:
            assert "products" in account_information
            for product in account_information:
                assert "id" in product
                assert "per_month_limit" in product
                assert "absolute_limit" in product
                assert "usage" in product
                assert "expiration_date" in product

    def test_account_information_using_proxy_with_basic_auth_should_fail_if_no_username_and_password_was_used(self):
        api.verify_ssl = False
        api.proxy_url = "http://localhost:8080"
        with pytest.raises(ProxyError):
            account_information = api.account_information()
            account_information.response()

    def test_account_information_using_proxy_with_basic_auth_should_fail_if_wrong_username_was_used(self):
        api.verify_ssl = False
        api.proxy_url = "http://wrongusername:pass@localhost:8080"
        with pytest.raises(ProxyError):
            account_information = api.account_information()
            account_information.response()

    def test_account_information_using_proxy_with_basic_auth_should_fail_if_wrong_password_was_used(self):
        api.verify_ssl = False
        api.proxy_url = "http://username:wrongpass@localhost:8080"
        with pytest.raises(ProxyError):
            account_information = api.account_information()
            account_information.response()

    def test_account_information_using_proxy_with_basic_auth_should_fail_if_wrong_username_and_password_were_used(self):
        api.verify_ssl = False
        api.proxy_url = "http://wrongusername:wrongpass@localhost:8080"
        with pytest.raises(ProxyError):
            account_information = api.account_information()
            account_information.response()
