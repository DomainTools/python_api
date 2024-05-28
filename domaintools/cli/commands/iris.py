import sys
import typer

from domaintools.cli.main import dt_cli
from domaintools.cli.api import DTCLICommand
from domaintools.cli.utils import (
    get_cli_helptext_by_name,
    remove_special_char_in_string,
)
from domaintools.cli import constants as c


@dt_cli.command(
    name=c.IRIS_INVESTIGATE,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_INVESTIGATE),
)
def iris_investigate(
    ctx: typer.Context,
    domains: str = typer.Option(None, "-d", "--domains", help="Domains to use."),
    data_updated_after: str = typer.Option(
        None, "--data-updated-after", help="The data updated after."
    ),
    expiration_date: str = typer.Option(
        None, "--expiration-date", help="The expiration date."
    ),
    create_date: str = typer.Option(None, "--create-date", help="The create date."),
    active: bool = typer.Option(
        None, "--active", help="The domains that are in active state"
    ),
    search_hash: str = typer.Option(
        None, "--search-hash", help="The search hash to use"
    ),
    src_file: str = typer.Option(
        None,
        "-s",
        "--source-file",
        help="Comma-separated list of maximum 100 domains. Supports only {.csv, .txt} format",
        callback=DTCLICommand.validate_source_file_extension,
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

    extra_args = ctx.args.copy()
    kwargs = DTCLICommand.args_to_dict(*extra_args)
    if "ssl_hash" in kwargs:
        # silently remove the ':' if present.
        ssl_hash_value = kwargs["ssl_hash"]
        kwargs["ssl_hash"] = remove_special_char_in_string(
            ssl_hash_value, special_char=":"
        )

    DTCLICommand.run(name=c.IRIS_INVESTIGATE, params=ctx.params, **kwargs)


@dt_cli.command(
    name="iris_enrich",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_ENRICH),
)
def iris_enrich(
    ctx: typer.Context,
    domains: str = typer.Option(None, "-d", "--domains", help="Domains to use."),
    src_file: str = typer.Option(
        None,
        "-s",
        "--source-file",
        help="Comma-separated list of maximum 100 domains. Supports only {.csv, .txt} format",
        callback=DTCLICommand.validate_source_file_extension,
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
    DTCLICommand.run(name=c.IRIS_ENRICH, params=ctx.params)


@dt_cli.command(
    name=c.IRIS,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help=get_cli_helptext_by_name(command_name=c.IRIS_ENRICH),
)
def iris(
    ctx: typer.Context,
    domain: str = typer.Option(None, "-d", "--domains", help="Domains to use."),
    ip: str = typer.Option(None, "--ip", help="IP to use."),
    email: str = typer.Option(None, "--email", help="Email to use."),
    nameserver: str = typer.Option(None, "--nameserver", help="Nameserver to use."),
    registrar: str = typer.Option(None, "--registrar", help="Registrar to use."),
    registrant: str = typer.Option(None, "--registrant", help="Registrant to use."),
    registrant_org: str = typer.Option(
        None, "--registrant-org", help="Registrant Org to use."
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
    params = ctx.params.copy()
    if (
        not params.get("domain")
        and not params.get("ip")
        and not params.get("email")
        and not params.get("nameserver")
        and not params.get("registrar")
        and not params.get("registrant")
        and not params.get("registrant_org")
    ):
        raise typer.BadParameter("At least one search term must be specified")

    DTCLICommand.run(name=c.IRIS, params=ctx.params)


__all__ = ["iris_investigate", "iris_enrich", "iris"]
