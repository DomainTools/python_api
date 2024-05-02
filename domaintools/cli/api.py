import time
import typer
import sys
import os
import _io

from typing import Optional, Dict, Tuple
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print

from domaintools.api import API
from domaintools.exceptions import ServiceException
from domaintools.cli.utils import get_file_extension


class DTCLICommand:
    API_SUCCESS_STATUS = 200
    APP_PARTNER_NAME = "python_wrapper_cli_2.0.0"

    @staticmethod
    def print_api_version(value: bool):
        if value:
            from domaintools._version import current as version

            print("DomainTools CLI API Client {0}".format(version))
            raise typer.Exit()

    @staticmethod
    def validate_format_input(value: str):
        VALID_FORMATS = ("list", "json", "xml", "html")
        if value not in VALID_FORMATS:
            raise typer.BadParameter(
                f"{value} is not in available formats: {VALID_FORMATS}"
            )
        return value

    @staticmethod
    def validate_source_file_extension(value: str):
        """Validates source file extension.

        Args:
            value (str): The source file (e.g. `my-domains.csv`).

        Raises:
            typer.BadParameter: Raises Badparameter exception if the given value is not in valid extensions.

        """
        if not value:
            return

        VALID_EXTENSIONS = (".csv", ".txt")
        ext = get_file_extension(value)

        if ext.lower() not in VALID_EXTENSIONS:
            raise typer.BadParameter(
                f"{value} is not in valid extensions. Valid file extensions: {VALID_EXTENSIONS}"
            )

        return value

    @staticmethod
    def args_to_dict(*args) -> Dict:
        """Converts args to key-value pair.

        Returns:
            Dict: The converted dictionary from args
        """
        argument_dict = {}
        if not args:
            return argument_dict

        try:
            for i in range(0, len(args), 2):
                key = args[i].replace("--", "")
                value = args[i + 1].strip()
                argument_dict[key] = value
        except:
            pass

        return argument_dict

    @classmethod
    def _get_formatted_output(cls, cmd_name: str, response, out_format: str = "json"):
        if cmd_name in ("available_api_calls",):
            return "\n".join(response)
        return str(
            getattr(response, out_format)
            if out_format != "list"
            else response.as_list()
        )

    @classmethod
    def _get_credentials(cls, params: Optional[Dict] = {}) -> Tuple[str]:
        user = params.pop("user")
        key = params.pop("key")

        if not user or not key:
            creds_file = params.pop("creds_file") or ""
            typer.echo(
                f"No user or key parameter given. Using credentials in {creds_file} instead."
            )

            try:
                if "~" in creds_file:
                    # expand user path if path uses "~".
                    creds_file = os.path.expanduser(creds_file)

                with open(creds_file, "r") as cf:
                    user, key = cf.readline().strip(), cf.readline().strip()
            except FileNotFoundError as e:
                raise typer.BadParameter(
                    f"{str(e)}. Please create one first and try again."
                )

        return user, key

    @classmethod
    def _get_domains_from_source(cls, source: str) -> Dict[str, str]:
        domains = []
        ext = get_file_extension(source)
        try:
            with open(source, "r", newline="", encoding="utf-8") as src:
                if ext == ".csv":
                    import csv

                    reader = csv.DictReader(src, fieldnames=("domain",))
                    next(reader)  # skip header
                    domains.extend([row.get("domain") or "" for row in reader])
                else:
                    domains.extend([domain.strip() for domain in src.readlines()])
        except FileNotFoundError:
            raise typer.BadParameter(f"File '{source}' not found.")

        return ",".join(domains)

    @classmethod
    def run(cls, name: str, params: Optional[Dict] = {}, **kwargs):
        """Run the domaintools command given with specified parameters.

        Args:
            name (str): The command name.
            params (Optional[Dict], optional): The command available parameters. Defaults to {}.
            kwargs (Optional[Dict], optional): The command available kwargs to pass in domaintools API
        """
        try:
            rate_limit = params.pop("rate_limit") or False
            response_format = params.pop("format") or "json"
            out_file = params.pop("out_file") or sys.stdout
            verify_ssl = params.pop("no_verify_ssl") or False
            source = None

            if "src_file" in params:
                source = params.pop("src_file") or None

            user, key = cls._get_credentials(params)

            # Add support for using a source file for commands that has `--domains` parameters
            if source:
                domains = cls._get_domains_from_source(source=source)
                if params["domains"]:
                    # append to existing domain parameter if found
                    params["domains"] = params["domains"] + "," + domains
                else:
                    params["domains"] = domains

            typer.echo(f"Using api credentials with a username of: {user}")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:

                progress.add_task(
                    description=f"Executing [green]{name}[/green] api call..."
                )

                dt_api = API(
                    user,
                    key,
                    app_name=cls.APP_PARTNER_NAME,
                    verify_ssl=verify_ssl,
                    rate_limit=rate_limit,
                )

                params = params | kwargs
                response = getattr(dt_api, name)(**params)
                progress.add_task(
                    description=f"Preparing results with format of {response_format}...",
                    total=0,
                )

                output = cls._get_formatted_output(
                    cmd_name=name, response=response, out_format=response_format
                )

                if isinstance(out_file, _io.TextIOWrapper):
                    # use rich `print` command to prettify the ouput in sys.stdout
                    print(output)
                else:
                    # if it's a file then write
                    out_file.write(output if output.endswith("\n") else output + "\n")
                time.sleep(0.5)

            name = typer.style(name, fg=typer.colors.CYAN, bold=True)
            typer.echo(f"Done fetching results from `{name}` command.")
        except Exception as e:
            if isinstance(e, ServiceException):
                code = typer.style(getattr(e, "code", 400), fg=typer.colors.BRIGHT_RED)
                _reason = getattr(e, "reason", {})
                # check data type first as some of the reasons is just plain text
                if isinstance(_reason, dict):
                    _reason = (
                        _reason.get("error", {}).get("message")
                        or "Unknown Error occured."
                    )

                reason = typer.style(_reason, bg=typer.colors.RED)

                err_msg_format = f"Error occured while fetching data from API: [{code}] Reason: {reason}"
                typer.echo(message=err_msg_format)
            else:
                typer.echo(message=e)
            return
