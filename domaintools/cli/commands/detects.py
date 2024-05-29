import sys
import typer

from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import get_cli_helptext_by_name
from domaintools.cli import constants as c


@dt_cli.command(
    name=c.IRIS_DETECT_MONITORS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_DETECT_MONITORS),
)
def iris_detect_monitors(
    ctx: typer.Context,
    include_counts: bool = typer.Option(
        False,
        "--include-counts",
        help="Includes counts for each monitor for new, watched, changed, and escalated domains",
    ),
    datetime_counts_since: str = typer.Option(
        None,
        "--datetime-counts-since",
        help="ISO-8601 date/time format. Conditionally required if the include_counts parameter is included. example: 2022-02-10",
    ),
    sort: str = typer.Option(
        None,
        "--sort",
        help="Provides options for sorting the monitor list. Available values : {term, created_date, domain_counts_changed, domain_counts_discovered}",
    ),
    order: str = typer.Option(
        "desc",
        "--order",
        help="Provides options for sorting the monitor list. Available values : {asc, desc}",
    ),
    offset: int = typer.Option(
        0, "--offset", help="For paginating requests beyond the limit."
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limit for pagination. Restricted to maximum 100 if include_counts is set to True.",
    ),
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    rate_limit: bool = typer.Option(
        False,
        "-l",
        "--rate_limit",
        help="Rate limit API calls against the API based on per minute limits.",
    ),
    format: str = typer.Option(
        "json",
        "-f",
        "--format",
        help="Output format in {'list', 'json', 'xml', 'html'}",
        callback=DTCLICommand.validate_format_input,
    ),
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):

    DTCLICommand.run(name=c.IRIS_DETECT_MONITORS, params=ctx.params)


@dt_cli.command(
    name=c.IRIS_DETECT_NEW_DOMAINS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_DETECT_NEW_DOMAINS),
)
def iris_detect_new_domains(
    ctx: typer.Context,
    monitor_id: str = typer.Option(
        None,
        "--monitor-id",
        help="Monitor ID from monitors response. Only used when requesting domains for a specific monitor.",
    ),
    tlds: str = typer.Option(
        None, "--tlds", help="Comma-separated TLDs to filter domains by."
    ),
    risk_score_ranges=typer.Option(
        None,
        "--risk-score-ranges",
        help='List of risk score ranges to filter domains by. Valid values are: ["0-0", "1-39", "40-69", "70-99", "100-100"]',
    ),
    mx_exists: bool = typer.Option(
        None, "--mx-exists", help="Filter domains by if they have an MX record in DNS."
    ),
    discovered_since: str = typer.Option(
        None,
        "--discovered-since",
        help="ISO 8601 datetime format: default None. Filter domains by when they were discovered.",
    ),
    changed_since: str = typer.Option(
        None,
        "--changed-since",
        help="""
        ISO 8601 datetime format: default None. Filter domains by when they were last changed. \n
        Most relevant for the iris_detect_watched_domains endpoint to control the timeframe for changes to DNS or whois
        fields for watched domains.
        """,
    ),
    search: str = typer.Option(
        None, "--search", help="A 'contains' search for any portion of a domain name."
    ),
    sort: str = typer.Option(
        None,
        "--sort",
        help='Sort order for domain list. Valid values are an ordered list of the following: {"discovered_date", "changed_date", "risk_score"}',
    ),
    order: str = typer.Option(None, "--order", help='Sort order "asc" or "desc"'),
    include_domain_data: bool = typer.Option(
        False,
        "--include-domain-data",
        help="Includes DNS and whois data in the response.",
    ),
    offset: int = typer.Option(
        0, "--offset", help="For paginating requests beyond the limit."
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limit for pagination. Restricted to maximum 100 if include_counts is set to True.",
    ),
    preview: bool = typer.Option(
        None,
        "--preview",
        help="Preview mode used for testing. If set to True, only the first 10 results are returned but not limited by hourly restrictions.",
    ),
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    rate_limit: bool = typer.Option(
        False,
        "-l",
        "--rate-limit",
        help="Rate limit API calls against the API based on per minute limits.",
    ),
    format: str = typer.Option(
        "json",
        "-f",
        "--format",
        help="Output format in {'list', 'json', 'xml', 'html'}",
        callback=DTCLICommand.validate_format_input,
    ),
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.IRIS_DETECT_NEW_DOMAINS, params=ctx.params)


@dt_cli.command(
    name=c.IRIS_DETECT_WATCHED_DOMAINS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_DETECT_WATCHED_DOMAINS),
)
def iris_detect_watched_domains(
    ctx: typer.Context,
    monitor_id: str = typer.Option(
        None,
        "--monitor-id",
        help="Monitor ID from monitors response. Only used when requesting domains for a specific monitor.",
    ),
    tlds: str = typer.Option(
        None, "--tlds", help="Comma-separated TLDs to filter domains by."
    ),
    escalation_types: str = typer.Option(
        None,
        "--escalation-types",
        help="List of escalation types to filter domains by. Valid values are: {'blocked', 'google_safe'}",
    ),
    escalated_since: str = typer.Option(
        None,
        "--escalated-since",
        help="""
        ISO 8601 datetime format: default None. Filter domains by when they were last escalated.
        Most relevant for the iris_detect_watched_domains endpoint to control the timeframe for when a domain was most
        recently escalated.
        """,
    ),
    risk_score_ranges=typer.Option(
        None,
        "--risk-score-ranges",
        help='List of risk score ranges to filter domains by. Valid values are: ["0-0", "1-39", "40-69", "70-99", "100-100"]',
    ),
    mx_exists: bool = typer.Option(
        None, "--mx-exists", help="Filter domains by if they have an MX record in DNS."
    ),
    discovered_since: str = typer.Option(
        None,
        "--discovered-since",
        help="ISO 8601 datetime format: default None. Filter domains by when they were discovered.",
    ),
    changed_since: str = typer.Option(
        None,
        "--changed-since",
        help="""
        ISO 8601 datetime format: default None. Filter domains by when they were last changed. \n
        Most relevant for the iris_detect_watched_domains endpoint to control the timeframe for changes to DNS or whois
        fields for watched domains.
        """,
    ),
    search: str = typer.Option(
        None, "--search", help="A 'contains' search for any portion of a domain name."
    ),
    sort: str = typer.Option(
        None,
        "--sort",
        help='Sort order for domain list. Valid values are an ordered list of the following: {"discovered_date", "changed_date", "risk_score"}',
    ),
    order: str = typer.Option(None, "--order", help='Sort order "asc" or "desc"'),
    include_domain_data: bool = typer.Option(
        False,
        "--include-domain-data",
        help="Includes DNS and whois data in the response.",
    ),
    offset: int = typer.Option(
        0, "--offset", help="For paginating requests beyond the limit."
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limit for pagination. Restricted to maximum 100 if include_counts is set to True.",
    ),
    preview: bool = typer.Option(
        None,
        "--preview",
        help="Preview mode used for testing. If set to True, only the first 10 results are returned but not limited by hourly restrictions.",
    ),
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    rate_limit: bool = typer.Option(
        False,
        "-l",
        "--rate-limit",
        help="Rate limit API calls against the API based on per minute limits.",
    ),
    format: str = typer.Option(
        "json",
        "-f",
        "--format",
        help="Output format in {'list', 'json', 'xml', 'html'}",
        callback=DTCLICommand.validate_format_input,
    ),
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.IRIS_DETECT_WATCHED_DOMAINS, params=ctx.params)


@dt_cli.command(
    name=c.IRIS_DETECT_MANAGE_WATCHLIST_DOMAINS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_DETECT_MANAGE_WATCHLIST_DOMAINS),
)
def iris_detect_manage_watchlist_domains(
    ctx: typer.Context,
    watchlist_domain_ids: str = typer.Option(
        None,
        "--watchlist-domain-ids",
        help="Comma-separated Iris Detect domain IDs to manage.",
    ),
    state: str = typer.Option(
        None, "--state", help="Valid values are: {'watched', 'ignored'}"
    ),
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    rate_limit: bool = typer.Option(
        False,
        "-l",
        "--rate-limit",
        help="Rate limit API calls against the API based on per minute limits.",
    ),
    format: str = typer.Option(
        "json",
        "-f",
        "--format",
        help="Output format in {'list', 'json', 'xml', 'html'}",
        callback=DTCLICommand.validate_format_input,
    ),
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.IRIS_DETECT_MANAGE_WATCHLIST_DOMAINS, params=ctx.params)


@dt_cli.command(
    name=c.IRIS_DETECT_ESCALATE_DOMAINS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_DETECT_ESCALATE_DOMAINS),
)
def iris_detect_escalate_domains(
    ctx: typer.Context,
    watchlist_domain_ids: str = typer.Option(
        None,
        "--watchlist-domain-ids",
        help="Comma-separated Iris Detect domain IDs to manage.",
    ),
    escalation_type: str = typer.Option(
        None,
        "--escalation-type",
        help="Escalation type to filter domains by. Valid values are: {'blocked', 'google_safe'}",
    ),
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    rate_limit: bool = typer.Option(
        False,
        "-l",
        "--rate-limit",
        help="Rate limit API calls against the API based on per minute limits.",
    ),
    format: str = typer.Option(
        "json",
        "-f",
        "--format",
        help="Output format in {'list', 'json', 'xml', 'html'}",
        callback=DTCLICommand.validate_format_input,
    ),
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.IRIS_DETECT_ESCALATE_DOMAINS, params=ctx.params)


@dt_cli.command(
    name=c.IRIS_DETECT_IGNORED_DOMAINS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_DETECT_IGNORED_DOMAINS),
)
def iris_detect_ignored_domains(
    ctx: typer.Context,
    monitor_id: str = typer.Option(
        None,
        "--monitor-id",
        help="Monitor ID from monitors response. Only used when requesting domains for a specific monitor.",
    ),
    tlds: str = typer.Option(
        None, "--tlds", help="Comma-separated TLDs to filter domains by."
    ),
    escalation_types: str = typer.Option(
        None,
        "--escalation-types",
        help="List of escalation types to filter domains by. Valid values are: {'blocked', 'google_safe'}",
    ),
    escalated_since: str = typer.Option(
        None,
        "--escalated-since",
        help="""
        ISO 8601 datetime format: default None. Filter domains by when they were last escalated.
        Most relevant for the iris_detect_watched_domains endpoint to control the timeframe for when a domain was most
        recently escalated.
        """,
    ),
    risk_score_ranges=typer.Option(
        None,
        "--risk-score-ranges",
        help='List of risk score ranges to filter domains by. Valid values are: ["0-0", "1-39", "40-69", "70-99", "100-100"]',
    ),
    mx_exists: bool = typer.Option(
        None, "--mx-exists", help="Filter domains by if they have an MX record in DNS."
    ),
    discovered_since: str = typer.Option(
        None,
        "--discovered-since",
        help="ISO 8601 datetime format: default None. Filter domains by when they were discovered.",
    ),
    changed_since: str = typer.Option(
        None,
        "--changed-since",
        help="""
        ISO 8601 datetime format: default None. Filter domains by when they were last changed. \n
        Most relevant for the iris_detect_watched_domains endpoint to control the timeframe for changes to DNS or whois
        fields for watched domains.
        """,
    ),
    search: str = typer.Option(
        None, "--search", help="A 'contains' search for any portion of a domain name."
    ),
    sort: str = typer.Option(
        None,
        "--sort",
        help='Sort order for domain list. Valid values are an ordered list of the following: {"discovered_date", "changed_date", "risk_score"}',
    ),
    order: str = typer.Option(None, "--order", help='Sort order "asc" or "desc"'),
    include_domain_data: bool = typer.Option(
        False,
        "--include-domain-data",
        help="Includes DNS and whois data in the response.",
    ),
    offset: int = typer.Option(
        0, "--offset", help="For paginating requests beyond the limit."
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limit for pagination. Restricted to maximum 100 if include_counts is set to True.",
    ),
    preview: bool = typer.Option(
        None,
        "--preview",
        help="Preview mode used for testing. If set to True, only the first 10 results are returned but not limited by hourly restrictions.",
    ),
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    rate_limit: bool = typer.Option(
        False,
        "-l",
        "--rate-limit",
        help="Rate limit API calls against the API based on per minute limits.",
    ),
    format: str = typer.Option(
        "json",
        "-f",
        "--format",
        help="Output format in {'list', 'json', 'xml', 'html'}",
        callback=DTCLICommand.validate_format_input,
    ),
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.IRIS_DETECT_IGNORED_DOMAINS, params=ctx.params)


__all__ = [
    "iris_detect_monitors",
    "iris_detect_new_domains",
    "iris_detect_watched_domains",
    "iris_detect_manage_watchlist_domains",
    "iris_detect_escalate_domains",
    "iris_detect_ignored_domains",
]
