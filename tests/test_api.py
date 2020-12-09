"""Tests the Python interface for DomainTools' APIs"""
from os import environ

import pytest
from domaintools import API, exceptions

from tests.settings import api, vcr


@vcr.use_cassette
def test_account_information():
    with api.account_information() as account_information:
        assert 'products' in account_information
        for product in account_information:
            assert 'id' in product
            assert 'per_month_limit' in product
            assert 'absolute_limit' in product
            assert 'usage' in product
            assert 'expiration_date' in product


@vcr.use_cassette
def test_available_api_calls():
    available_api_calls = api.available_api_calls()
    # Not sure what else to check for as this is highly dependent on your API_KEY but at least account_information
    # should be there.
    assert 'account_information' in available_api_calls


@vcr.use_cassette
def test_brand_monitor():
    api_call = api.brand_monitor('google')
    with api_call as response:
        assert 'query' in response
        assert 'limit' in response
        assert 'total' in response
        assert 'exclude' in response
        assert 'new' in response
        assert 'on-hold' in response
        assert 'utf8' in response
        assert 'date' in response

        for alert in api_call:
            assert 'domain' in alert
            assert 'status' in alert


@vcr.use_cassette
def test_domain_profile():
    with api.domain_profile('google.com') as response:
        assert 'history' in response
        assert 'server' in response
        assert 'name_servers' in response
        assert 'website_data' in response
        assert 'seo' in response
        assert 'registration' in response
        assert 'registrant' in response

        history = response['history']
        assert 'whois' in history
        assert 'registrar' in history
        assert 'name_server' in history
        assert 'ip_address' in history


@vcr.use_cassette
def test_domain_search():
    api_call = api.domain_search('google')
    with api_call as response:
        assert 'results' in response
        assert 'query_info' in response

        for domain in api_call:
            assert 'hashad_tlds' in domain
            assert 'has_number' in domain
            assert 'char_count' in domain
            assert 'tlds' in domain
            assert 'sld' in domain
            assert 'has_deleted' in domain
            assert 'has_active' in domain
            assert 'has_hyphen' in domain
            assert 'tlds_count' in domain

    exclude_list = ['domaintools', 'ff1toolsdomain']
    api_call = api.domain_search('domain tools', exclude_query=exclude_list)
    with api_call as response:

        for domain in response:
            assert domain['sld'] not in exclude_list


@vcr.use_cassette
def test_domain_suggestions():
    api_call = api.domain_suggestions('google')
    with api_call as response:
        assert 'status_codes' in response
        assert 'suggestions' in response
        assert 'query' in response
        assert 'tlds' in response

        for suggestion in api_call:
            assert 'domain' in suggestion
            assert 'status' in suggestion


@vcr.use_cassette
def test_hosting_history():
    api_call = api.hosting_history('google.com')
    with api_call as result:
        assert 'domain_name' in result
        assert 'registrar_history' in result
        assert 'nameserver_history' in result
        assert 'ip_history' in result

        for history_section, history_item in api_call:
            assert str(history_section)
            assert isinstance(history_item, dict)


@vcr.use_cassette
def test_ip_monitor():
    api_call = api.ip_monitor('65.55.53.233')
    with api_call as results:
        assert results['ip_address'] == '65.55.53.233'
        assert 'alerts' in results
        assert 'date' in results
        assert 'limit' in results
        assert 'page' in results
        assert 'page_count' in results
        assert 'total' in results

        for result in api_call:
            assert result


@vcr.use_cassette
def test_name_server_monitor():
    api_call = api.name_server_monitor('google.com')
    with api_call as results:
        assert 'limit' in results
        assert 'date' in results
        assert 'name_server' in results
        assert 'total' in results
        assert 'page' in results
        assert 'alerts' in results

        for alert in api_call:
            assert alert


@vcr.use_cassette
def test_parsed_whois():
    api_call = api.parsed_whois('google.com')
    with api_call as result:
        assert 'registrant' in result
        assert 'registration' in result
        assert 'name_servers' in result
        assert 'whois' in result
        assert 'parsed_whois' in result
        assert 'record_source' in result

        for key, value in api_call.items():
            assert key

        assert isinstance(result.flattened(), dict)


@vcr.use_cassette
def test_registrant_monitor():
    api_call = api.registrant_monitor('google')
    with api_call as result:
        assert 'query' in result
        assert 'limit' in result
        assert 'total' in result
        assert 'date' in result
        assert 'alerts' in result

        for alert in api_call:
            assert 'domain' in alert
            assert 'match_type' in alert
            assert 'current_owner' in alert
            assert 'created' in alert
            assert 'modified' in alert
            assert 'last_owner' in alert


@vcr.use_cassette
def test_reputation():
    api_call = api.reputation('google.com')
    with api_call as risk_data:
        assert risk_data['risk_score'] == 0
        assert risk_data['domain'] == 'google.com'
        assert int(api_call) == 0
        assert float(api_call) == 0.0


@vcr.use_cassette
def test_reverse_ip():
    with api.reverse_ip('google.com') as results:
        assert 'ip_addresses' in results


@vcr.use_cassette
def test_host_domains():
    with api.host_domains(ip='199.30.228.112') as results:
        assert 'ip_addresses' in results


@vcr.use_cassette
def test_reverse_ip_whois():
    api_call = api.reverse_ip_whois(query='Domain Tools')
    with api_call as results:
        assert 'page' in results
        assert 'has_more_pages' in results
        assert 'record_count' in results
        assert 'records' in results

        for record in api_call:
            assert 'ip_to' in record
            assert 'country' in record
            assert 'organization' in record
            assert 'record_date' in record
            assert 'range' in record
            assert 'record_ip' in record
            assert 'server' in record
            assert 'ip_from' in record

        assert len(api_call) > 0

    with api.reverse_ip_whois(ip='65.55.53.233') as result:
        assert 'ip_to_alloc' in result
        assert 'range' in result
        assert 'ip_from_alloc' in result
        assert 'server' in result
        assert 'whois_record' in result
        assert 'organization' in result
        assert 'record_date' in result
        assert 'country' in result
        assert 'ip_to' in result
        assert 'ip_from' in result

    with pytest.raises(ValueError):
        api.reverse_ip_whois(ip='8.8.8.8', query='Google')


@vcr.use_cassette
def test_reverse_name_server():
    api_call = api.reverse_name_server('google.com')
    with api_call as result:
        assert 'name_server' in result
        assert 'primary_domains' in result
        assert 'secondary_domains' in result

        for primary_domain in api_call:
            assert primary_domain


@vcr.use_cassette
def test_reverse_whois():
    api_call = api.reverse_whois('Amazon')
    with api_call as result:
        assert 'domain_count' in result

        for domain in result:
            assert domain


@vcr.use_cassette
def test_whois():
    api_call = api.whois('google.com')
    with api_call as whois:
        assert 'registrant' in whois
        assert 'name_servers' in whois
        assert 'whois' in whois
        assert 'record_source' in whois

        assert 'abusecomplaints@markmonitor.com' in api_call.emails()


@vcr.use_cassette
def test_whois_history():
    api_call = api.whois_history('woot.com')
    with api_call as results:
        assert 'record_count' in results
        assert 'history' in results

        for history_item in api_call:
            assert 'date' in history_item
            assert 'is_private' in history_item
            assert 'whois' in history_item


@vcr.use_cassette
def test_dict_like_behaviour():
    with api.whois('google.com') as whois_google:
        assert len(whois_google.items())
        assert len(whois_google.keys())
        assert len(whois_google.values())
        assert whois_google.has_key('registrant')
        assert 'registrant' in whois_google
        whois_google.update({'registrant': 'override'})
        assert whois_google['registrant'] == 'override'
        del whois_google['registrant']
        assert not 'registrant' in whois_google
        whois_google['registrant'] = 'me'
        assert whois_google['registrant'] == 'me'
        assert isinstance(whois_google.pop('whois', {}), dict)


@vcr.use_cassette
def test_list_like_behaviour():
    with api.phisheye('google') as data:
        data.insert(0, {'domain': 'woot', 'tld': 'com'})
        assert data['term'] == 'google'
        for result in data:
            assert result['domain']
            assert result['tld']


@vcr.use_cassette
def test_exception_handling():
    exception = None
    api_call = api.reverse_ip('ss')
    assert api_call.status == 400
    try:
        api_call.data()
    except Exception as e:
        exception = e

    assert exception
    assert exception.code == 400
    assert 'not understand' in exception.reason['error']['message']

    with pytest.raises(exceptions.NotFoundException):
        api._results('i_made_this_product_up', '/v1/steianrstierstnrsiatiarstnsto.com/whois').data()
    with pytest.raises(exceptions.NotAuthorizedException):
        API('notauser', 'notakey').domain_search('amazon').data()
    with pytest.raises(ValueError, match=r"Invalid value 'notahash' for 'key_sign_hash'. Values available are sha1,sha256,md5"):
        API('notauser', 'notakey', always_sign_api_key=True, key_sign_hash='notahash').domain_search('amazon')



@vcr.use_cassette
def test_rate_limiting():
    domain_searches = ['google'] * 31
    for domain_search in domain_searches:
        api.domain_search(domain_search).data()


@vcr.use_cassette
def test_no_https():
    try:
        no_https_api = API(environ.get('TEST_USER', 'test_user'), environ.get('TEST_KEY', 'test_key'), https=False)
        assert no_https_api.domain_search('google').data()
    except exceptions.NotAuthorizedException:
        pass


@vcr.use_cassette
def test_formats():
    with api.domain_search('google') as data:
        assert '{' in str(data.json)
        assert '<' in str(data.xml)
        assert '<title>' in str(data.html)
        assert '\n' in str(data.as_list())


@vcr.use_cassette
def test_phisheye():
    with api.phisheye('google') as data:
        assert data['term'] == 'google'
        for result in data:
            assert result['domain']
            assert result['tld']


@vcr.use_cassette
def test_phisheye_term_list():
    with api.phisheye_term_list() as data:
        assert data
        for term in data:
            assert 'term' in term
            assert type(term['active']) == bool


@vcr.use_cassette
def test_iris():
    with pytest.raises(ValueError):
        api.iris()

    with api.iris(domain='google.com', https=False) as results:
        assert results
        for result in results:
            assert 'domain' in result
            assert str(result['domain'])


@vcr.use_cassette
def test_risk():
    with api.risk(domain='google.com') as result:
        assert result
        assert int(result) == 0

    with api.risk(domain='hug.rest') as result:
        assert result
        assert int(result) > 0


@vcr.use_cassette
def test_risk_evidence():
    with api.risk_evidence(domain='google.com') as result:
        assert result
        assert list(result) == [{'name': 'whitelist', 'risk_score': 0}]


@vcr.use_cassette
def test_iris_enrich():
    with pytest.raises(ValueError):
        api.iris_enrich()

    enriched_data = api.iris_enrich('google.com')
    assert enriched_data['results_count']
    for result in enriched_data:
        assert result['domain'] == 'google.com'


@vcr.use_cassette
def test_iris_investigate():
    with pytest.raises(ValueError):
        api.iris_investigate()

    investigation_results = api.iris_investigate(domains=['amazon.com', 'google.com'])
    assert investigation_results['results_count']
    for result in investigation_results:
        assert result['domain'] == 'amazon.com' or result['domain'] == 'google.com'


@vcr.use_cassette
def test_limit_exceeded():
    with pytest.raises(exceptions.ServiceException):
        response = api.iris_investigate(ip="8.8.8.8")
        response.response()
