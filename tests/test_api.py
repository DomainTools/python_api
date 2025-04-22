"""Tests the Python interface for DomainTools APIs"""

from os import environ

import json
import pytest

from inspect import isgenerator

from domaintools import API, exceptions
from tests.settings import api, feeds_api, vcr


@vcr.use_cassette
def test_account_information():
    with api.account_information() as account_information:
        assert "products" in account_information
        for product in account_information:
            assert "id" in product
            assert "per_month_limit" in product
            assert "absolute_limit" in product
            assert "usage" in product
            assert "expiration_date" in product


@vcr.use_cassette
def test_available_api_calls():
    available_api_calls = api.available_api_calls()
    # Not sure what else to check for as this is highly dependent on your API_KEY but at least account_information
    # should be there.
    assert "account_information" in available_api_calls


@vcr.use_cassette
def test_brand_monitor():
    api_call = api.brand_monitor("google")
    with api_call as response:
        assert "query" in response
        assert "limit" in response
        assert "total" in response
        assert "exclude" in response
        assert "new" in response
        assert "on-hold" in response
        assert "utf8" in response
        assert "date" in response

        for alert in api_call:
            assert "domain" in alert
            assert "status" in alert


@vcr.use_cassette
def test_domain_profile():
    with api.domain_profile("google.com") as response:
        assert "history" in response
        assert "server" in response
        assert "name_servers" in response
        assert "website_data" in response
        assert "seo" in response
        assert "registration" in response
        assert "registrant" in response

        history = response["history"]
        assert "whois" in history
        assert "registrar" in history
        assert "name_server" in history
        assert "ip_address" in history


@vcr.use_cassette
def test_domain_search():
    api_call = api.domain_search("google")
    with api_call as response:
        assert "results" in response
        assert "query_info" in response

        for domain in api_call:
            assert "hashad_tlds" in domain
            assert "has_number" in domain
            assert "char_count" in domain
            assert "tlds" in domain
            assert "sld" in domain
            assert "has_deleted" in domain
            assert "has_active" in domain
            assert "has_hyphen" in domain
            assert "tlds_count" in domain

    exclude_list = ["domaintools", "ff1toolsdomain"]
    api_call = api.domain_search("domain tools", exclude_query=exclude_list)
    with api_call as response:

        for domain in response:
            assert domain["sld"] not in exclude_list


@vcr.use_cassette
def test_hosting_history():
    api_call = api.hosting_history("google.com")
    with api_call as result:
        assert "domain_name" in result
        assert "registrar_history" in result
        assert "nameserver_history" in result
        assert "ip_history" in result

        for history_section, history_item in api_call:
            assert str(history_section)
            assert isinstance(history_item, dict)


@vcr.use_cassette
def test_ip_monitor():
    api_call = api.ip_monitor("65.55.53.233")
    with api_call as results:
        assert results["ip_address"] == "65.55.53.233"
        assert "alerts" in results
        assert "date" in results
        assert "limit" in results
        assert "page" in results
        assert "page_count" in results
        assert "total" in results

        for result in api_call:
            assert result


@vcr.use_cassette
def test_name_server_monitor():
    api_call = api.name_server_monitor("google.com")
    with api_call as results:
        assert "limit" in results
        assert "date" in results
        assert "name_server" in results
        assert "total" in results
        assert "page" in results
        assert "alerts" in results

        for alert in api_call:
            assert alert


@vcr.use_cassette
def test_parsed_whois():
    api_call = api.parsed_whois("google.com")
    with api_call as result:
        assert "registrant" in result
        assert "registration" in result
        assert "name_servers" in result
        assert "whois" in result
        assert "parsed_whois" in result
        assert "record_source" in result

        for key, value in api_call.items():
            assert key

        assert isinstance(result.flattened(), dict)


@vcr.use_cassette
def test_parsed_domain_rdap():
    api_call = api.parsed_domain_rdap("google.com")
    with api_call as result:
        for key in (
            "handle",
            "domain_statuses",
            "creation_date",
            "last_changed_date",
            "expiration_date",
            "nameservers",
            "conformance",
            "emails",
            "email_domains",
            "unclassified_emails",
            "registrar",
            "contacts",
        ):
            assert key in result.get("parsed_domain_rdap")

        for key, value in result.items():
            assert key

        assert isinstance(result.flattened(), dict)


@vcr.use_cassette
def test_registrant_monitor():
    api_call = api.registrant_monitor("google")
    with api_call as result:
        assert "query" in result
        assert "limit" in result
        assert "total" in result
        assert "date" in result
        assert "alerts" in result

        for alert in api_call:
            assert "domain" in alert
            assert "match_type" in alert
            assert "current_owner" in alert
            assert "created" in alert
            assert "modified" in alert
            assert "last_owner" in alert


@vcr.use_cassette
def test_reputation():
    api_call = api.reputation("google.com")
    with api_call as risk_data:
        assert risk_data["risk_score"] == 0
        assert risk_data["domain"] == "google.com"
        assert int(api_call) == 0
        assert float(api_call) == 0.0


@vcr.use_cassette
def test_reverse_ip():
    with api.reverse_ip("google.com") as results:
        assert "ip_addresses" in results


@vcr.use_cassette
def test_host_domains():
    with api.host_domains(ip="199.30.228.112") as results:
        assert "ip_addresses" in results


@vcr.use_cassette
def test_reverse_ip_whois():
    api_call = api.reverse_ip_whois(query="DomainTools")
    with api_call as results:
        assert "page" in results
        assert "has_more_pages" in results
        assert "record_count" in results
        assert "records" in results

        for record in api_call:
            assert "ip_to" in record
            assert "country" in record
            assert "organization" in record
            assert "record_date" in record
            assert "range" in record
            assert "record_ip" in record
            assert "server" in record
            assert "ip_from" in record

        assert len(api_call) > 0

    with api.reverse_ip_whois(ip="65.55.53.233") as result:
        assert "ip_to_alloc" in result
        assert "range" in result
        assert "ip_from_alloc" in result
        assert "server" in result
        assert "whois_record" in result
        assert "organization" in result
        assert "record_date" in result
        assert "country" in result
        assert "ip_to" in result
        assert "ip_from" in result

    with pytest.raises(ValueError):
        api.reverse_ip_whois(ip="8.8.8.8", query="Google")


@vcr.use_cassette
def test_reverse_name_server():
    api_call = api.reverse_name_server("google.com")
    with api_call as result:
        assert "name_server" in result
        assert "primary_domains" in result
        assert "secondary_domains" in result

        for primary_domain in api_call:
            assert primary_domain


@vcr.use_cassette
def test_reverse_whois():
    api_call = api.reverse_whois("Google")
    with api_call as result:
        assert "domain_count" in result

        for domain in result:
            assert domain


@vcr.use_cassette
def test_whois():
    api_call = api.whois("google.com")
    with api_call as whois:
        assert "registrant" in whois
        assert "name_servers" in whois
        assert "whois" in whois
        assert "record_source" in whois

        assert "abusecomplaints@markmonitor.com" in api_call.emails()


@vcr.use_cassette
def test_whois_history():
    api_call = api.whois_history("woot.com")
    with api_call as results:
        assert "record_count" in results
        assert "history" in results

        for history_item in api_call:
            assert "date" in history_item
            assert "is_private" in history_item
            assert "whois" in history_item


@vcr.use_cassette
def test_dict_like_behaviour():
    with api.whois("google.com") as whois_google:
        assert len(whois_google.items())
        assert len(whois_google.keys())
        assert len(whois_google.values())
        assert "registrant" in whois_google
        whois_google.update({"registrant": "override"})
        assert whois_google["registrant"] == "override"
        del whois_google["registrant"]
        assert "registrant" not in whois_google
        whois_google["registrant"] = "me"
        assert whois_google["registrant"] == "me"
        assert isinstance(whois_google.pop("whois", {}), dict)


@vcr.use_cassette
def test_exception_handling():
    exception = None
    api_call = api.reverse_ip("ss")
    assert api_call.status == 400
    try:
        api_call.data()
    except Exception as e:
        exception = e

    assert exception
    assert exception.code == 400
    assert "not understand" in exception.reason["error"]["message"]

    with pytest.raises(exceptions.NotFoundException):
        api._results("i_made_this_product_up", "/v1/steianrstierstnrsiatiarstnsto.com/whois").data()
    with pytest.raises(exceptions.NotAuthorizedException):
        API("notauser", "notakey").domain_search("amazon").data()
    with pytest.raises(
        ValueError,
        match=r"Invalid value 'notahash' for 'key_sign_hash'. Values available are sha1,sha256,md5",
    ):
        API("notauser", "notakey", always_sign_api_key=True, key_sign_hash="notahash").domain_search("amazon")


@vcr.use_cassette
def test_rate_limiting():
    domain_searches = ["google"] * 31
    for domain_search in domain_searches:
        api.domain_search(domain_search).data()


@vcr.use_cassette
def test_no_https():
    with pytest.raises(
        Exception,
        match=r"The DomainTools API endpoints no longer support http traffic. Please make sure https=True.",
    ):
        API(
            environ.get("TEST_USER", "test_user"),
            environ.get("TEST_KEY", "test_key"),
            https=False,
        )


@vcr.use_cassette
def test_formats():
    with api.domain_search("google") as data:
        assert "{" in str(data.json)
        assert "<" in str(data.xml)
        assert "<title>" in str(data.html)
        assert "\n" in str(data.as_list())


@vcr.use_cassette
def test_iris():
    with pytest.raises(ValueError):
        api.iris()

    with api.iris(domain="google.com") as results:
        assert results
        for result in results:
            assert "domain" in result
            assert str(result["domain"])


@vcr.use_cassette
def test_risk():
    with api.risk(domain="google.com") as result:
        assert result
        assert int(result) == 0

    with api.risk(domain="hug.rest") as result:
        assert result
        assert int(result) > 0


@vcr.use_cassette
def test_risk_evidence():
    with api.risk_evidence(domain="google.com") as result:
        assert result
        assert list(result) == [{"name": "zerolist", "risk_score": 0}]


@vcr.use_cassette
def test_iris_enrich():
    with pytest.raises(ValueError):
        api.iris_enrich()

    enriched_data = api.iris_enrich("google.com")
    assert enriched_data["results_count"]
    for result in enriched_data:
        assert result["domain"] == "google.com"


@vcr.use_cassette
def test_iris_enrich_cli():
    with pytest.raises(ValueError):
        api.iris_enrich()

    enriched_data = api.iris_enrich("google.com")
    assert enriched_data["results_count"]
    for result in enriched_data:
        assert result["domain"] == "google.com"


@vcr.use_cassette
def test_iris_investigate():
    with pytest.raises(ValueError):
        api.iris_investigate()

    investigation_results = api.iris_investigate(domains=["amazon.com", "google.com"])
    assert investigation_results["results_count"]
    for result in investigation_results:
        assert result["domain"] in ["amazon.com", "google.com"]


@vcr.use_cassette
def test_iris_detect_monitors():
    with pytest.raises(ValueError):
        api.iris_detect_monitors(include_counts=True)

    detect_results = api.iris_detect_monitors()
    assert detect_results["total_count"] >= 1

    detect_results = api.iris_detect_monitors(sort=["domain_counts_discovered", "term"])
    assert detect_results["monitors"][0]["term"] == "google"


@vcr.use_cassette
def test_iris_detect_new_domains():
    detect_results = api.iris_detect_new_domains(monitor_id="nAwmQg2pqg", sort=["risk_score"], order="desc")
    assert detect_results["watchlist_domains"][0]["risk_score"] == 100


@vcr.use_cassette
def test_iris_detect_watched_domains():
    detect_results = api.iris_detect_watched_domains()
    assert detect_results["count"] >= 0

    detect_results = api.iris_detect_watched_domains(monitor_id="nAwmQg2pqg", sort=["risk_score"], order="desc")
    assert len(detect_results["watchlist_domains"]) == 2

    detect_results = api.iris_detect_watched_domains(escalation_types="blocked")
    assert detect_results["count"] == 1


@vcr.use_cassette
def test_iris_detect_manage_watchlist_domains():
    detect_results = api.iris_detect_manage_watchlist_domains(watchlist_domain_ids=["gae08rdVWG"], state="watched")
    assert detect_results["watchlist_domains"][0]["state"] == "watched"


@vcr.use_cassette
def test_iris_detect_escalate_domains():
    # If you rerun this test without VCR, it will fail because the domain is already escalated
    detect_results = api.iris_detect_escalate_domains(watchlist_domain_ids=["OWxzqKqQEY"], escalation_type="blocked")
    assert detect_results["escalations"][0]["escalation_type"] == "blocked"

    detect_results = api.iris_detect_escalate_domains(watchlist_domain_ids=["OWxzqKqQEY"], escalation_type="google_safe")
    assert detect_results["escalations"][0]["escalation_type"] == "google_safe"


@vcr.use_cassette
def test_iris_detect_ignored_domains():
    detect_results = api.iris_detect_ignored_domains()
    assert detect_results["count"] >= 1

    detect_results = api.iris_detect_ignored_domains(monitor_id="DKObxJVjYJ")
    assert detect_results["count"] >= 1


@vcr.use_cassette
def test_limit_exceeded():
    with pytest.raises(exceptions.ServiceException):
        response = api.iris_investigate(ip="8.8.8.8")
        response.response()


@vcr.use_cassette
def test_newly_observed_domains_feed():
    results = feeds_api.nod(after="-60", header_authentication=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()


@vcr.use_cassette
def test_newly_observed_hosts_feed():
    results = feeds_api.noh(after="-60", header_authentication=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()


@vcr.use_cassette
def test_newly_observed_domains_feed_pagination():
    results = feeds_api.nod(sessionID="integrations-testing", after="2025-01-16T10:20:00Z")
    page_count = 0
    for response in results.response():
        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        page_count += 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()

    assert page_count > 1


@vcr.use_cassette
def test_newly_active_domains_feed():
    results = feeds_api.nad(after="-60", header_authentication=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()


@vcr.use_cassette
def test_domainrdap_feed():
    results = feeds_api.domainrdap(after="-60", top=2, header_authenticationn=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")

        assert response is not None
        assert len(rows) == 2

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()
            assert "parsed_record" in feed_result.keys()
            assert "domain" in feed_result["parsed_record"]["parsed_fields"]
            assert "emails" in feed_result["parsed_record"]["parsed_fields"]
            assert "contacts" in feed_result["parsed_record"]["parsed_fields"]


@vcr.use_cassette
def test_domain_discovery_feed():
    results = feeds_api.domaindiscovery(after="-60", header_authentication=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()


@vcr.use_cassette
def test_domainrdap_feed_not_api_header_auth():
    results = feeds_api.domainrdap(after="-60", sessiondID="integrations-testing", top=5, header_authenticationn=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")

        assert response is not None
        assert len(rows) == 5

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()
            assert "parsed_record" in feed_result.keys()
            assert "domain" in feed_result["parsed_record"]["parsed_fields"]
            assert "emails" in feed_result["parsed_record"]["parsed_fields"]
            assert "contacts" in feed_result["parsed_record"]["parsed_fields"]


@vcr.use_cassette
def test_verify_response_is_a_generator():
    results = feeds_api.domaindiscovery(after="-60", header_authenticationn=False)

    assert isgenerator(results.response())


@vcr.use_cassette
def test_feeds_endpoint_should_non_header_auth_be_the_default():
    results = feeds_api.domaindiscovery(after="-60", endpoint="download")
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "download_name" in feed_result["response"].keys()
            assert "files" in feed_result["response"].keys()


@vcr.use_cassette
def test_feeds_endpoint_should_raise_error_if_no_required_params():
    with pytest.raises(ValueError) as excinfo:
        feeds_api.domaindiscovery()

    assert str(excinfo.value) == "sessionID or after or before must be provided"


@vcr.use_cassette
def test_feeds_endpoint_should_raise_error_if_asked_csv_format_for_download_api():
    with pytest.raises(ValueError) as excinfo:
        feeds_api.domaindiscovery(after="-60", output_format="csv", endpoint="download")

    assert str(excinfo.value) == "csv format is not available in download API."


@vcr.use_cassette
def test_realtime_domain_risk():
    results = feeds_api.realtime_domain_risk(after="-60", header_authentication=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()
            assert "phishing_risk" in feed_result.keys()
            assert "malware_risk" in feed_result.keys()
            assert "proximity_risk" in feed_result.keys()
            assert "overall_risk" in feed_result.keys()


@vcr.use_cassette
def test_domain_hotlist():
    results = feeds_api.domainhotlist(after="-60", header_authentication=False)
    for response in results.response():
        assert results.status == 200

        rows = response.strip().split("\n")
        assert response is not None
        assert len(rows) >= 1

        for row in rows:
            feed_result = json.loads(row)
            assert "timestamp" in feed_result.keys()
            assert "domain" in feed_result.keys()
            assert "phishing_risk" in feed_result.keys()
            assert "malware_risk" in feed_result.keys()
            assert "proximity_risk" in feed_result.keys()
            assert "overall_risk" in feed_result.keys()
