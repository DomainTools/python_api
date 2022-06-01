from datetime import datetime
import dateparser


def get_domain_age(create_date):
    """
    Finds how many days old a domain is given a start date.
    Args:
        create_date: Date in the form of %Y-%m-%d'

    Returns: Number of days between now and the create_date.
    """
    time_diff = datetime.now() - dateparser.parse(create_date, date_formats=['%Y-%m-%d', '%Y%m%d'])

    return time_diff.days


def get_threat_component(components, threat_type):
    """
    Gets a certain threat component out a list of components
    Args:
        components: List of threat components
        threat_type: Type of threat we are looking for

    Returns: Either the component that we asked for or None
    """
    for component in components:
        if component.get("name") == threat_type:
            return component
    else:
        return None


def get_average_risk_score(domains):
    """
    Gets average domain risk score for Investigate and Detect result sets
    Args:
        domains: Investigate or Detect result set

    Returns: average risk score
    """
    count = 0
    total = 0
    for d in domains:
        # investigate result set
        if "risk_score" in d.get("domain_risk", {}):
            count += 1
            total += d.get("domain_risk").get("risk_score")
        # detect result set
        elif d.get("risk_score"):
            count += 1
            total += d.get("risk_score")

    return total // count if count else None


def get_average_age(domains):
    """
    Gets average domain age for Investigate and Detect result sets
    Args:
        domains: Investigate or Detect result set

    Returns: average age
    """
    count = 0
    total = 0
    for d in domains:
        if isinstance(d.get("create_date"), dict) and d.get("create_date").get("value"):
            count += 1
            total += get_domain_age(d.get("create_date").get("value"))
        elif isinstance(d.get("create_date"), int):
            count += 1
            total += get_domain_age(str(d.get("create_date")))

    return total // count if count else None
