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
