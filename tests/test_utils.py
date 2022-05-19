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