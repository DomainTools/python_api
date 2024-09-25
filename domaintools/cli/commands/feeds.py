import sys
import typer


from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import get_cli_helptext_by_name
from domaintools.cli import constants as c


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
    no_sign_api_key: bool = typer.Option(
        True,
        "--no-sign-api-key",
        help="Skip signing of api key",
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
    no_sign_api_key: bool = typer.Option(
        True,
        "--no-sign-api-key",
        help="Skip signing of api key",
    ),
):
    DTCLICommand.run(name=c.FEEDS_NOD, params=ctx.params)
