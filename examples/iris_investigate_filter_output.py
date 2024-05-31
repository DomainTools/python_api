from domaintools import API


dt_api = API(USER_NAME, KEY)
domains = "int-chase.com, google.com"


def sample_filter_by_risk_score():
    """
    Sample code snippet on how to use the output filtering by a given riskscore
    """
    response = dt_api.iris_investigate(domains=domains, risk_score=68)
    output_domains = [
        (result.get("domain"), result.get("domain_risk", {}).get("risk_score"))
        for result in response.get("results") or []
    ]
    # this will output [('int-chase.com', 71)], assuming that this domain has a >= to the given riskscore
    print(f"Filter by `risk_score` result: {output_domains}")


def sample_filter_by_younger_than_date():
    """
    Sample code snippet on how to use the output filtering by younger_than_date.
    The field being used in this filter is the `expiration_date`.
    """
    response = dt_api.iris_investigate(domains=domains, younger_than_date="2024-02-24")

    output_domains = [
        (result.get("domain"), result.get("expiration_date"))
        for result in response.get("results") or []
    ]
    # this will output [('google.com', {'value': '2028-09-14', 'count': 9972})],
    # assuming that this domain has a expiration_date <= to the given date.
    print(f"Filter by `younger_than_date` result: {output_domains}")


def sample_filter_by_older_than_date():
    """
    Sample code snippet on how to use the output filtering by older_than_date.
    The field being used in this filter is the `expiration_date`.
    """
    response = dt_api.iris_investigate(domains=domains, older_than_date="2024-02-24")

    output_domains = [
        (result.get("domain"), result.get("expiration_date"))
        for result in response.get("results") or []
    ]
    # this will output  [('int-chase.com', {'value': '2021-10-13', 'count': 118259})],
    # assuming that this domain has a expiration_date <= to the given date.
    print(f"Filter by `older_than_date` result: {output_domains}")


def sample_filter_by_updated_after():
    """
    Sample code snippet on how to use the output filtering by updated_after.
    The field being used in this filter is the `data_updated_timestamp`.
    """
    response = dt_api.iris_investigate(domains=domains, updated_after="2024-02-24")

    output_domains = [
        (result.get("domain"), result.get("data_updated_timestamp"))
        for result in response.get("results") or []
    ]
    # this will output  [('google.com', {'value': '2028-09-14', 'count': 9972})],
    # assuming that this domain has a data_updated_timestamp >= to the given `updated_after` date.
    print(f"Filter by `updated_after` result: {output_domains}")


def sample_filter_by_include_domains_with_missing_field():
    """
    Sample code snippet on how to use the output filtering to include
    the domain even the given field is missing or empty in the result set.
    """
    response = dt_api.iris_investigate(
        domains=domains, include_domains_with_missing_field="popularity_rank"
    )

    # this will output  [('google.com', 1), ('int-chase.com', '')]
    output_domains = [
        (result.get("domain"), result.get("popularity_rank"))
        for result in response.get("results") or []
    ]
    print(f"Filter by `include_domains_with_missing_field` result: {output_domains}")


def sample_filter_by_exclude_domains_with_missing_field():
    """
    Sample code snippet on how to use the output filtering to exclude
    the domain even the given field is missing or empty in the result set.
    """
    response = dt_api.iris_investigate(
        domains=domains, exclude_domains_with_missing_field="popularity_rank"
    )

    # this will only output [('google.com', 1)] as the popularity rank in other domain is missing/empty
    output_domains = [
        (result.get("domain"), result.get("popularity_rank"))
        for result in response.get("results") or []
    ]
    print(f"Filter by `exclude_domains_with_missing_field` result: {output_domains}")


sample_filter_by_risk_score()
sample_filter_by_younger_than_date()
sample_filter_by_older_than_date()
sample_filter_by_updated_after()
sample_filter_by_include_domains_with_missing_field()
sample_filter_by_exclude_domains_with_missing_field()
