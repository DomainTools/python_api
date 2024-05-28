import sys
import typer


from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import get_cli_helptext_by_name
from domaintools.cli import constants as c


@dt_cli.command(
    name=c.PHISHEYE,
    help=get_cli_helptext_by_name(command_name=c.PHISHEYE),
)
def phisheye(
    ctx: typer.Context,
    query: str = typer.Option(..., "-q", "--query", help="The domain to query."),
    days_back: str = typer.Option(
        None,
        "--days-back",
        help="Use this parameter in exceptional circumstances where you need to search domains registered up to six days prior to the current date. Set the value to an integer in the range of 1-6.",
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
    DTCLICommand.run(name=c.PHISHEYE, params=ctx.params)


@dt_cli.command(
    name=c.PHISHEYE_TERM_LIST,
    help=get_cli_helptext_by_name(command_name=c.PHISHEYE_TERM_LIST),
)
def phisheye_termlist(
    ctx: typer.Context,
    include_inactive: bool = typer.Option(
        False,
        "--include-inactive",
        help="Use this parameter to display terms that may have been inactivated in users' lists.",
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
    DTCLICommand.run(name=c.PHISHEYE_TERM_LIST, params=ctx.params)


__all__ = ["phisheye", "phisheye_termlist"]
