from datetime import datetime
import dateparser


def get_domain_age(create_date):
    """
    Finds how many days old a domain is given a start date.
    Args:
        create_date: Date in the form of %Y-%m-%d'

    Returns: Number of days between now and the create_date.
    """
    time_diff = datetime.now() - dateparser.parse(create_date)
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