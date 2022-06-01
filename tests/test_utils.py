from datetime import datetime, timedelta
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


def test_enrich_and_investigate_average_risk_score():
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