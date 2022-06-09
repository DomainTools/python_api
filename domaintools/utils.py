from datetime import datetime
import dateparser
import re


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


def prune_data(data_obj):
    """
    Does a deep dive through a data object to prune any null or empty items. Checks for empty lists, dicts, and strs.
    Args:
        data_obj: Either a list or dict that needs to be pruned
    """
    items_to_prune = []
    if isinstance(data_obj, dict) and len(data_obj):
        for k, v in data_obj.items():
            if isinstance(data_obj[k], dict) or isinstance(data_obj[k], list):
                prune_data(data_obj[k])
            if not isinstance(v, int) and not v:
                items_to_prune.append(k)
            elif k == 'count' and v == 0:
                items_to_prune.append(k)
        for k in items_to_prune:
            del data_obj[k]
    elif isinstance(data_obj, list) and len(data_obj):
        for index, item in enumerate(data_obj):
            prune_data(item)
            if not isinstance(item, int) and not item:
                items_to_prune.append(index)
        data_obj[:] = [item for index, item in enumerate(data_obj) if index not in items_to_prune and len(item)]


def find_emails(data_str):
    """Find and returns all emails"""
    return set(re.findall(r'[\w\.-]+@[\w\.-]+', data_str))


def find_ips(data_str):
    """Find and returns all ipv4"""
    ipv4s = set(re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', data_str))
    return ipv4s

