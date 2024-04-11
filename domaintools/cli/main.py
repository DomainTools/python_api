import typer
import sys
import os

from domaintools.cli.api import DTCLICommand


dt_cli = typer.Typer()

# import all other commands
from domaintools.cli.commands import *


@dt_cli.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "-v",
        "--version",
        callback=DTCLICommand.print_api_version,
        help="Show Domaintools CLI version information.",
    ),
):
    print(f"About to execute command: `{ctx.invoked_subcommand}`")


__all__ = ["dt_cli"]
