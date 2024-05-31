import sys
import typer


from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import get_cli_helptext_by_name
from domaintools.cli import constants as c


@dt_cli.command(
    name=c.IP_MONITOR,
    help=get_cli_helptext_by_name(command_name=c.IP_MONITOR),
)
def ip_monitor(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The IP address to query."),
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
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.IP_MONITOR, params=ctx.params)


@dt_cli.command(
    name=c.IP_REGISTRANT_MONITOR,
    help=get_cli_helptext_by_name(command_name=c.IP_REGISTRANT_MONITOR),
)
def ip_registrant_monitor(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The IP address to query."),
    days_back: int = typer.Option(0, "--days-back", help=""),
    page: int = typer.Option(1, "--page", help=""),
    search_type: str = typer.Option("all", "--search-type", help="The search type."),
    server: str = typer.Option(None, "--server", help="The server name"),
    country: str = typer.Option(None, "--country", help="The country name"),
    org: str = typer.Option(None, "--org", help="The country name"),
    include_total_count: bool = typer.Option(
        False,
        "--include-total-count",
        help="This will include the total count.",
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
    DTCLICommand.run(name=c.IP_REGISTRANT_MONITOR, params=ctx.params)


@dt_cli.command(
    name=c.HOST_DOMAINS,
    help=get_cli_helptext_by_name(command_name=c.HOST_DOMAINS),
)
def host_domains(
    ctx: typer.Context,
    ip: str = typer.Option(..., "--ip", help="The IP address to query."),
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
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.HOST_DOMAINS, params=ctx.params)


@dt_cli.command(
    name=c.REVERSE_IP_WHOIS,
    help=get_cli_helptext_by_name(command_name=c.REVERSE_IP_WHOIS),
)
def reverse_ip_whois(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The IP address to query."),
    ip: str = typer.Option(0, "--ip", help="The IP address to query."),
    country: str = typer.Option(None, "--country", help="The country name"),
    server: str = typer.Option(None, "--server", help="The server name"),
    include_total_count: bool = typer.Option(
        False,
        "--include-total-count",
        help="This will include the total count.",
    ),
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
    out_file: typer.FileTextWrite = typer.Option(
        sys.stdout, "-o", "--out-file", help="Output file (defaults to stdout)"
    ),
    no_verify_ssl: bool = typer.Option(
        False,
        "--no-verify-ssl",
        help="Skip verification of SSL certificate when making HTTPs API calls",
    ),
):
    DTCLICommand.run(name=c.REVERSE_IP_WHOIS, params=ctx.params)


__all__ = ["ip_monitor", "ip_registrant_monitor", "host_domains", "reverse_ip_whois"]
