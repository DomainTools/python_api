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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    # Result formatting parameters
    # Note: the Parsed Domain RDAP feed returns JSON only; CSV format and headers are not supported.
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    overall_min: int = typer.Option(
        None,
        "--overall-min",
        help="Minimum overall combined risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    malware_min: int = typer.Option(
        None,
        "--malware-min",
        help="Minimum malware risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    phishing_min: int = typer.Option(
        None,
        "--phishing-min",
        help="Minimum phishing risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    spam_min: int = typer.Option(
        None,
        "--spam-min",
        help="Minimum spam risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    proximity_min: int = typer.Option(
        None,
        "--proximity-min",
        help="Minimum proximity risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint. For risk feeds, results are sorted by all_threats_combined_percent (descending)",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
    ),
    page: int = typer.Option(
        None,
        "--page",
        help="Selects which page of results to return (0-indexed). Only applies to the download endpoint.",
    ),
    prefix: str = typer.Option(
        None,
        "--prefix",
        help="Filters results by date using the file prefix. Only applies to the download endpoint.",
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    domain: str = typer.Option(
        None,
        "-d",
        "--domain",
        help="A string value used to filter feed results",
    ),
    overall_min: int = typer.Option(
        None,
        "--overall-min",
        help="Minimum overall combined risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    malware_min: int = typer.Option(
        None,
        "--malware-min",
        help="Minimum malware risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    phishing_min: int = typer.Option(
        None,
        "--phishing-min",
        help="Minimum phishing risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    spam_min: int = typer.Option(
        None,
        "--spam-min",
        help="Minimum spam risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    proximity_min: int = typer.Option(
        None,
        "--proximity-min",
        help="Minimum proximity risk score (1-99). Combined with other risk filters as a logical AND",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint. For risk feeds, results are sorted by all_threats_combined_percent (descending)",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
    ),
    page: int = typer.Option(
        None,
        "--page",
        help="Selects which page of results to return (0-indexed). Only applies to the download endpoint.",
    ),
    prefix: str = typer.Option(
        None,
        "--prefix",
        help="Filters results by date using the file prefix. Only applies to the download endpoint.",
    ),
):
    DTCLICommand.run(name=c.FEEDS_REALTIME_DOMAIN_RISK, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_IPHOTLIST,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_IPHOTLIST),
)
def feeds_iphotlist(
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    pdns_resolutions_min: int = typer.Option(
        None,
        "--pdns-resolutions-min",
        help="Minimum number of distinct domains actively resolving to the IP within the last 24 hours (positive integer)",
    ),
    bad_pdns_resolutions_min: int = typer.Option(
        None,
        "--bad-pdns-resolutions-min",
        help="Minimum number of confirmed bad (malicious) domains actively resolving to the IP within the last 24 hours (positive integer)",
    ),
    total_domains_max: int = typer.Option(
        None,
        "--total-domains-max",
        help="Maximum number of total domains hosted on the IP (positive integer). Useful for filtering out superhosters such as CDNs or large hosting providers",
    ),
    third_party_threats_min: int = typer.Option(
        None,
        "--third-party-threats-min",
        help="Minimum number of hosted domains independently confirmed as threats on external third-party intelligence feeds (positive integer)",
    ),
    all_threats_combined_percent_min: int = typer.Option(
        None,
        "--all-threats-combined-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as malicious across all threat types",
    ),
    combined_phishing_percent_min: int = typer.Option(
        None,
        "--combined-phishing-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as phishing",
    ),
    combined_malware_percent_min: int = typer.Option(
        None,
        "--combined-malware-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as malware",
    ),
    combined_spam_percent_min: int = typer.Option(
        None,
        "--combined-spam-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as spam",
    ),
    all_threats_percent_min: int = typer.Option(
        None,
        "--all-threats-percent-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed with threats across all threat types",
    ),
    percent_phishing_min: int = typer.Option(
        None,
        "--percent-phishing-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed as phishing",
    ),
    percent_malware_min: int = typer.Option(
        None,
        "--percent-malware-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed as malware",
    ),
    percent_spam_min: int = typer.Option(
        None,
        "--percent-spam-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed as spam",
    ),
    asn: int = typer.Option(
        None,
        "--asn",
        help="Autonomous System Number (digits only, e.g. 15169). Restricts output to IPs belonging to a specific routing provider/network. No AS prefix and wildcards are not supported",
    ),
    organization: str = typer.Option(
        None,
        "--organization",
        help="Full exact name of the organization (e.g. Example Hosting Inc). Matches the exact string only; wildcards are not supported",
    ),
    country_code: str = typer.Option(
        None,
        "--country-code",
        help="Case-sensitive two-letter country code (e.g. CN, US, NL). Filters results to IPs geolocated to that country",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint. For risk feeds, results are sorted by all_threats_combined_percent (descending)",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
    ),
    page: int = typer.Option(
        None,
        "--page",
        help="Selects which page of results to return (0-indexed). Only applies to the download endpoint.",
    ),
    prefix: str = typer.Option(
        None,
        "--prefix",
        help="Filters results by date using the file prefix. Only applies to the download endpoint.",
    ),
):
    DTCLICommand.run(name=c.FEEDS_IPHOTLIST, params=ctx.params)


@dt_cli.command(
    name=c.FEEDS_IPRISK,
    help=get_cli_helptext_by_name(command_name=c.FEEDS_IPRISK),
)
def feeds_iprisk(
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
    no_header_authentication: bool = typer.Option(
        False,
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
    # Session Management Parameters
    sessionID: str = typer.Option(
        None,
        "--session-id",
        help="Unique identifier for the session. Required when using --frombeginning",
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
        help="End of the query window (inclusive). Integer from -1 to -432000 (seconds before now) or an absolute ISO 8601 UTC datetime. The window covers at most the most recent 5 days",
        callback=DTCLICommand.validate_after_or_before_input,
    ),
    fromBeginning: bool = typer.Option(
        None,
        "-fb",
        "--frombeginning",
        help="Requires a sessionID. When used with a new session ID, returns the first hour of data in the time window (rather than the last). Returns an error if the session ID already exists",
    ),
    # Filter Parameters
    pdns_resolutions_min: int = typer.Option(
        None,
        "--pdns-resolutions-min",
        help="Minimum number of distinct domains actively resolving to the IP within the last 24 hours (positive integer)",
    ),
    bad_pdns_resolutions_min: int = typer.Option(
        None,
        "--bad-pdns-resolutions-min",
        help="Minimum number of confirmed bad (malicious) domains actively resolving to the IP within the last 24 hours (positive integer)",
    ),
    total_domains_max: int = typer.Option(
        None,
        "--total-domains-max",
        help="Maximum number of total domains hosted on the IP (positive integer). Useful for filtering out superhosters such as CDNs or large hosting providers",
    ),
    third_party_threats_min: int = typer.Option(
        None,
        "--third-party-threats-min",
        help="Minimum number of hosted domains independently confirmed as threats on external third-party intelligence feeds (positive integer)",
    ),
    all_threats_combined_percent_min: int = typer.Option(
        None,
        "--all-threats-combined-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as malicious across all threat types",
    ),
    combined_phishing_percent_min: int = typer.Option(
        None,
        "--combined-phishing-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as phishing",
    ),
    combined_malware_percent_min: int = typer.Option(
        None,
        "--combined-malware-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as malware",
    ),
    combined_spam_percent_min: int = typer.Option(
        None,
        "--combined-spam-percent-min",
        help="Minimum percentage (0-100) of hosted domains confirmed or predicted as spam",
    ),
    all_threats_percent_min: int = typer.Option(
        None,
        "--all-threats-percent-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed with threats across all threat types",
    ),
    percent_phishing_min: int = typer.Option(
        None,
        "--percent-phishing-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed as phishing",
    ),
    percent_malware_min: int = typer.Option(
        None,
        "--percent-malware-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed as malware",
    ),
    percent_spam_min: int = typer.Option(
        None,
        "--percent-spam-min",
        help="Minimum percentage (0-100) of hosted domains actively confirmed as spam",
    ),
    asn: int = typer.Option(
        None,
        "--asn",
        help="Autonomous System Number (digits only, e.g. 15169). Restricts output to IPs belonging to a specific routing provider/network. No AS prefix and wildcards are not supported",
    ),
    organization: str = typer.Option(
        None,
        "--organization",
        help="Full exact name of the organization (e.g. Example Hosting Inc). Matches the exact string only; wildcards are not supported",
    ),
    country_code: str = typer.Option(
        None,
        "--country-code",
        help="Case-sensitive two-letter country code (e.g. CN, US, NL). Filters results to IPs geolocated to that country",
    ),
    # Result formatting parameters
    output_format: str = typer.Option(
        "jsonl",
        "-f",
        "--format",
        help=f"Output format in [{OutputFormat.JSONL.value}, {OutputFormat.CSV.value}]",
        callback=DTCLICommand.validate_feeds_format_input,
    ),
    headers: bool = typer.Option(
        False,
        "--headers",
        help="Adds a header to the first line of response when text/csv is set in header parameters",
    ),
    top: int = typer.Option(
        None,
        "--top",
        help="Number of results to return in the response payload. This is ignored in download endpoint. For risk feeds, results are sorted by all_threats_combined_percent (descending)",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        help="Limits the number of files returned in the response. Only applies to the download endpoint.",
    ),
    page: int = typer.Option(
        None,
        "--page",
        help="Selects which page of results to return (0-indexed). Only applies to the download endpoint.",
    ),
    prefix: str = typer.Option(
        None,
        "--prefix",
        help="Filters results by date using the file prefix. Only applies to the download endpoint.",
    ),
):
    DTCLICommand.run(name=c.FEEDS_IPRISK, params=ctx.params)
