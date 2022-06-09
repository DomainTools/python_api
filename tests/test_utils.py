import json
from datetime import datetime, timedelta

from tests.responses.expected_data import prune_espn_expected
from tests.responses.iris_investage_data import espn
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
    data = espn()
    utils.prune_data(data)
    assert data == prune_espn_expected()


def test_find_emails():
    emails = utils.find_emails(json.dumps(espn()))
    assert emails == {'domainabuse@cscglobal.com', 'awsdns-hostmaster@amazon.com', 'domreg@espn.com'}


def test_find_ips():
    ips = utils.find_ips(json.dumps(espn()))
    assert ips == {'104.47.44.36',
                   '104.47.45.36',
                   '13.224.13.26',
                   '13.224.13.62',
                   '13.224.13.66',
                   '13.224.13.80',
                   '205.251.192.122',
                   '205.251.195.78',
                   '205.251.196.21',
                   '205.251.199.144',
                   '74.123.200.120',
                   '74.123.200.222',
                   '74.123.200.35',
                   '74.123.200.36',
                   '74.123.203.125',
                   '74.123.203.98',
                   '99.86.32.125',
                   '99.86.32.27',
                   '99.86.32.32',
                   '99.86.32.4'}
