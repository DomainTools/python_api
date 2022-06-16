import json
from datetime import datetime, timedelta

from tests.responses import iris_investigate_data
from tests.responses.expected_data import prune_domaintools_expected
from tests.settings import utils


def test_get_domain_age():
    create_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result = utils.get_domain_age(create_date)
    assert result == 1


def test_get_threat_component():
    threat_components = [
        {"name": "threat_profile_malware", "risk_score": 31},
        {"name": "threat_profile_spam", "risk_score": 73, "threats": ["spam"]}
    ]
    result = utils.get_threat_component(threat_components, "threat_profile_malware")
    assert result.get("risk_score") == 31


def test_investigate_average_risk_score():
    domains = [
        {"domain_risk": {"risk_score": 25}},
        {"domain_risk": {"risk_score": 27}}
    ]
    result = utils.get_average_risk_score(domains)
    assert result == 26

    domains = [
        {"domain_risk": {"risk_score": 25}},
        {}
    ]
    result = utils.get_average_risk_score(domains)
    assert result == 25

    domains = []
    result = utils.get_average_risk_score(domains)
    assert result == None


def test_detect_average_risk_score():
    domains = [
        {"risk_score": 25},
        {"risk_score": 27}
    ]
    result = utils.get_average_risk_score(domains)
    assert result == 26

    domains = [
        {"risk_score": 25},
        {"risk_score": None}
    ]
    result = utils.get_average_risk_score(domains)
    assert result == 25

    domains = []
    result = utils.get_average_risk_score(domains)
    assert result == None


def test_investigate_average_age():
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    five_days_ago = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

    domains = [
        {"create_date": {"value": two_days_ago}},
        {"create_date": {"value": five_days_ago}}
    ]
    result = utils.get_average_age(domains)
    assert result == 3

    domains = [
        {"create_date": {"value": two_days_ago}},
        {}
    ]
    result = utils.get_average_age(domains)
    assert result == 2

    domains = [
        {"create_date": {"value": two_days_ago}},
        {"create_date": {"value": ""}}
    ]
    result = utils.get_average_age(domains)
    assert result == 2

    domains = []
    result = utils.get_average_age(domains)
    assert result == None


def test_detect_average_age():
    two_days_ago = int((datetime.now() - timedelta(days=2)).strftime("%Y%m%d"))
    five_days_ago = int((datetime.now() - timedelta(days=5)).strftime("%Y%m%d"))
    domains = [
        {"create_date": two_days_ago},
        {"create_date": five_days_ago}
    ]
    result = utils.get_average_age(domains)
    assert result == 3

    domains = [
        {"create_date": two_days_ago},
        {"create_date": None}
    ]
    result = utils.get_average_age(domains)
    assert result == 2

    domains = []
    result = utils.get_average_risk_score(domains)
    assert result == None


def test_data_prune():
    data = iris_investigate_data.domaintools()
    utils.prune_data(data)
    assert data == prune_domaintools_expected()


def test_find_emails():
    emails = utils.find_emails(json.dumps(iris_investigate_data.domaintools()))
    assert emails == {'abuse@enom.com', 'hostmaster@nsone.net'}


def test_find_ips():
    ips = utils.find_ips(json.dumps(iris_investigate_data.domaintools()))
    assert ips == {'142.250.115.26',
                   '142.250.141.27',
                   '198.51.44.4',
                   '198.51.44.68',
                   '198.51.45.4',
                   '198.51.45.68',
                   '199.30.228.112',
                   '64.233.171.26',
                   '74.125.142.26'}

def test_get_pivots():
    pivots = utils.get_pivots(iris_investigate_data.domaintools().get("results"), "")
    assert pivots == [
        ['IP ADDRESS', ('199.30.228.112', 4)],
        ['IP ASN', (17318, 111)],
        ['IP ISP', ('DomainTools LLC', 222)]
    ]

