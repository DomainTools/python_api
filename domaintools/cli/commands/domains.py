import sys
import typer


from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import get_cli_helptext_by_name
from domaintools.cli import constants as c


@dt_cli.command(
    name=c.BRAND_MONITOR,
    help=get_cli_helptext_by_name(command_name=c.BRAND_MONITOR),
)
def brand_monitor(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The query to use."),
    exclude: str = typer.Option(None, "--exclude", help="The exclude condition."),
    domain_status: str = typer.Option(None, "--domain-status", help="The domain status."),
    days_back: int = typer.Option(None, "--days-back", help="The days back to check."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.BRAND_MONITOR, params=ctx.params)


@dt_cli.command(
    name=c.DOMAIN_PROFILE,
    help=get_cli_helptext_by_name(command_name=c.DOMAIN_PROFILE),
)
def domain_profile(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain name to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.DOMAIN_PROFILE, params=ctx.params)


@dt_cli.command(
    name=c.DOMAIN_SEARCH,
    help=get_cli_helptext_by_name(command_name=c.DOMAIN_SEARCH),
)
def domain_search(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain name to query."),
    exclude_query: str = typer.Option(None, "--exclude-query", help="The exclusion filter to query."),
    max_length: int = typer.Option(25, "--max-length", help="The max length"),
    min_length: int = typer.Option(2, "--min-length", help="The min length"),
    has_hyphen: bool = typer.Option(True, "--has-hyphen", help=""),
    has_number: bool = typer.Option(True, "--has-number", help=""),
    active_only: bool = typer.Option(False, "--active-only", help="Search for active only domains."),
    deleted_only: bool = typer.Option(False, "--deleted-only", help="Search for deleted only domains."),
    anchor_left: bool = typer.Option(False, "--achor-left", help=""),
    anchor_right: bool = typer.Option(False, "--achor-right", help=""),
    page: int = typer.Option(1, "--page", help="Number of pages to return."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.DOMAIN_SEARCH, params=ctx.params)


@dt_cli.command(
    name=c.HOSTING_HISTORY,
    help=get_cli_helptext_by_name(command_name=c.HOSTING_HISTORY),
)
def hosting_history(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain name to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        True,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.HOSTING_HISTORY, params=ctx.params)


@dt_cli.command(
    name=c.NAME_SERVER_MONITOR,
    help=get_cli_helptext_by_name(command_name=c.NAME_SERVER_MONITOR),
)
def name_server_monitor(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The nameserver to query."),
    days_back: int = typer.Option(0, "--days-back", help=""),
    page: int = typer.Option(1, "--page", help=""),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.NAME_SERVER_MONITOR, params=ctx.params)


@dt_cli.command(
    name=c.PARSED_WHOIS,
    help=get_cli_helptext_by_name(command_name=c.PARSED_WHOIS),
)
def parsed_whois(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.PARSED_WHOIS, params=ctx.params)


@dt_cli.command(
    name=c.PARSED_DOMAIN_RDAP,
    help=get_cli_helptext_by_name(command_name=c.PARSED_DOMAIN_RDAP),
)
def parsed_domain_rdap(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.PARSED_DOMAIN_RDAP, params=ctx.params)


@dt_cli.command(
    name=c.REGISTRANT_MONITOR,
    help=get_cli_helptext_by_name(command_name=c.REGISTRANT_MONITOR),
)
def registrant_monitor(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The query to use."),
    exclude: str = typer.Option(None, "--exclude", help="The exclude condition."),
    days_back: str = typer.Option(None, "--days-back", help="The days back to check."),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Specify the maximum number of records to retrieve in an API query.",
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.REGISTRANT_MONITOR, params=ctx.params)


@dt_cli.command(
    name=c.REPUTATION,
    help=get_cli_helptext_by_name(command_name=c.REPUTATION),
)
def reputation(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain to query."),
    include_reasons: bool = typer.Option(False, "--include-reasons", help=""),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.REPUTATION, params=ctx.params)


@dt_cli.command(
    name=c.REVERSE_IP,
    help=get_cli_helptext_by_name(command_name=c.REVERSE_IP),
)
def reverse_ip(
    ctx: typer.Context,
    domain: str = typer.Option(..., "-d", "--domain", help="The domain to query."),
    limit: int = typer.Option(None, "--limit", help=""),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.REVERSE_IP, params=ctx.params)


@dt_cli.command(
    name=c.REVERSE_NAME_SERVER,
    help=get_cli_helptext_by_name(command_name=c.REVERSE_NAME_SERVER),
)
def reverse_nameserver(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain to query."),
    limit: int = typer.Option(None, "--limit", help=""),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.REVERSE_NAME_SERVER, params=ctx.params)


@dt_cli.command(
    name=c.REVERSE_WHOIS,
    help=get_cli_helptext_by_name(command_name=c.REVERSE_WHOIS),
)
def reverse_whois(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain to query."),
    exclude: str = typer.Option(None, "--exclude", help="The exclude condition."),
    scope: str = typer.Option(
        "current",
        "--scope",
        help="Sets the scope of the report to include only current Whois records, or to include both current and historic records.",
    ),
    mode: str = typer.Option("purchase", "--mode", help="Values must be purchase (the default) or quote"),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.REVERSE_WHOIS, params=ctx.params)


@dt_cli.command(
    name=c.WHOIS,
    help=get_cli_helptext_by_name(command_name=c.WHOIS),
)
def whois(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain or IP to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.WHOIS, params=ctx.params)


@dt_cli.command(
    name=c.WHOIS_HISTORY,
    help=get_cli_helptext_by_name(command_name=c.WHOIS_HISTORY),
)
def whois_history(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain or IP to query."),
    mode: str = typer.Option(
        None,
        "--mode",
        help="An optional parameter that changes the mode of the API result. Available values: {check_existence, count, list}",
    ),
    sort: str = typer.Option(
        None,
        "--sort",
        help="Sort the records returned in either ascending or descending order. Available values: {date_asc, date _desc}",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Specify the maximum number of records to retrieve in an API query.",
    ),
    offset: int = typer.Option(None, "--offset", help="For paginating requests beyond the limit."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.WHOIS_HISTORY, params=ctx.params)


@dt_cli.command(
    name=c.RISK,
    help=get_cli_helptext_by_name(command_name=c.RISK),
)
def risk(
    ctx: typer.Context,
    domain: str = typer.Option(..., "-d", "--domain", help="The domain to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.RISK, params=ctx.params)


@dt_cli.command(
    name=c.RISK_EVIDENCE,
    help=get_cli_helptext_by_name(command_name=c.RISK_EVIDENCE),
)
def risk_evidence(
    ctx: typer.Context,
    domain: str = typer.Option(..., "-d", "--domain", help="The domain to query."),
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
    out_file: typer.FileTextWrite = typer.Option(sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.RISK_EVIDENCE, params=ctx.params)


__all__ = [
    "brand_monitor",
    "domain_profile",
    "domain_search",
    "name_server_monitor",
    "parsed_whois",
    "parsed_domain_rdap",
    "registrant_monitor",
    "reputation",
    "reverse_ip",
    "reverse_nameserver",
    "reverse_whois",
    "whois",
    "whois_history",
    "risk",
    "risk_evidence",
]
