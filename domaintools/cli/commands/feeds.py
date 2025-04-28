import typer


from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import get_cli_helptext_by_name
from domaintools.cli import constants as c
from domaintools.constants import Endpoint, OutputFormat


@dt_cli.command(
    name=c.FEEDS_NAD,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_NAD),
)
def feeds_nad(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
):
    DTCLICommand.run(name=c.FEEDS_NAD, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_NOD,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_NOD),
)
def feeds_nod(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
):
    DTCLICommand.run(name=c.FEEDS_NOD, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_DOMAINRDAP,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_DOMAINRDAP),
)
def feeds_domainrdap(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload",
    ),
):
    DTCLICommand.run(name=c.FEEDS_DOMAINRDAP, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_DOMAINDISCOVERY,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_DOMAINDISCOVERY),
)
def feeds_domaindiscovery(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
):
    DTCLICommand.run(name=c.FEEDS_DOMAINDISCOVERY, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_NOH,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_NOH),
)
def feeds_noh(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
):
    DTCLICommand.run(name=c.FEEDS_NOH, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_DOMAINHOTLIST,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_DOMAINHOTLIST),
)
def feeds_domainhotlist(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
):
    DTCLICommand.run(name=c.FEEDS_DOMAINHOTLIST, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_REALTIME_DOMAIN_RISK,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_REALTIME_DOMAIN_RISK),
)
def feeds_realtime_domain_risk(
    ctx: typer.Context,
    user: str = typer.Option(None, "-u", "--user", help="Domaintools API Username."),
    key: str = typer.Option(None, "-k", "--key", help="DomainTools API key"),
    creds_file: str = typer.Option(
        "~/.dtapi",
        "-c",
        "--credfile",
        help="Optional file with API username and API key, one per line.",
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
    no_sign_api_key: bool = typer.Option(
        False,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
    header_authentication: bool = typer.Option(
        True,
        "--no-header-auth",
        help="Don't use header authentication",
    ),
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    endpoint: str = typer.Option(
        Endpoint.FEED.value,
        "-e",
        "--endpoint",
        help=f"Valid endpoints: [{Endpoint.FEED.value}, {Endpoint.DOWNLOAD.value}]",
        callback=DTCLICommand.validate_endpoint_input,
    ),
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session",
    ),
    after: str = typer.Option(
        None,
        "--after",
        help="Start of the time window, relative to the current time in seconds, for which data will be provided",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    before: str = typer.Option(
        None,
        "--before",
        help="The end of the query window in seconds, relative to the current time, inclusive",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: str = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
):
    DTCLICommand.run(name=c.FEEDS_REALTIME_DOMAIN_RISK, params=ctx.params)
