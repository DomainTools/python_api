import time
import typer
import sys
import os
import _io

from datetime import datetime
from typing import Optional, Dict, Tuple
from rich.progress import Progress, SpinnerColumn, TextColumn

from domaintools.api import API
from domaintools.constants import Endpoint, FEEDS_PRODUCTS_LIST, OutputFormat
from domaintools.cli.utils import get_file_extension
from domaintools.exceptions import ServiceException
from domaintools._version import current as version


class DTCLICommand:
    API_SUCCESS_STATUS = 200
    APP_PARTNER_NAME = f"python_wrapper_cli_{version}"

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
            raise typer.BadParameter(f"{value} is not in available formats: {VALID_FORMATS}")
        return value

    @staticmethod
    def validate_feeds_format_input(value: str):
        VALID_FEEDS_FORMATS = ("jsonl", "csv")
        if value not in VALID_FEEDS_FORMATS:
            raise typer.BadParameter(f"{value} is not in available formats: {VALID_FEEDS_FORMATS}")
        return value

    @staticmethod
    def validate_endpoint_input(value: str):
        VALID_ENDPOINTS = (Endpoint.FEED.value, Endpoint.DOWNLOAD.value)
        if value not in VALID_ENDPOINTS:
            raise typer.BadParameter(f"{value} is not in available endpoints: {VALID_ENDPOINTS}")
        return value

    @staticmethod
    def validate_after_or_before_input(value: str):
        if value is None or value.replace("-", "").isdigit():
            return value

        # Checks if value is a valid ISO 8601 datetime string in UTC form
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            return value
        except:
            raise typer.BadParameter(f"{value} is neither an integer or a valid ISO 8601 datetime string in UTC form")

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
            raise typer.BadParameter(f"{value} is not in valid extensions. Valid file extensions: {VALID_EXTENSIONS}")

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
                # replace all the "-" to "_" to make it a valid kwargs
                # we replace all CLI parameters to use "-" instead of underscore.
                key = key.replace("-", "_")
                argument_dict[key] = value
        except:
            pass

        return argument_dict

    @classmethod
    def _get_formatted_output(cls, cmd_name: str, response, out_format: str = "json"):
        if cmd_name in ("available_api_calls",):
            return "\n".join(response)
        if response.product in FEEDS_PRODUCTS_LIST:
            return "\n".join([data for data in response.response()])
        return str(getattr(response, out_format) if out_format != "list" else response.as_list())

    @classmethod
    def _get_credentials(cls, params: Optional[Dict] = {}) -> Tuple[str]:
        user = params.pop("user")
        key = params.pop("key")
        creds_file = params.pop("creds_file", {}) or ""

        if not user or not key:
            try:
                if "~" in creds_file:
                    # expand user path if path uses "~".
                    creds_file = os.path.expanduser(creds_file)

                with open(creds_file, "r") as cf:
                    user, key = cf.readline().strip(), cf.readline().strip()
            except FileNotFoundError as e:
                raise typer.BadParameter(f"{str(e)}. Please create one first and try again.")

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

                total_domains_found = len(domains)
                if total_domains_found > 100:
                    raise typer.BadParameter(
                        f"Domains in source file exceeds the maximum count of 100. Current source file domain count: {total_domains_found}"
                    )

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
            rate_limit = params.pop("rate_limit", False)
            response_format = (
                params.pop("format", "json")
                if params.get("format", None)
                else params.get(
                    "output_format", OutputFormat.JSONL.value
                )  # Using output_format for RTUF endpoints to separate from other endpoints. This will be needed further along the process
            )
            out_file = params.pop("out_file", sys.stdout)
            verify_ssl = params.pop("no_verify_ssl", False)
            always_sign_api_key = params.pop("no_sign_api_key", False)
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

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:

                progress.add_task(
                    description=f"Using api credentials with a username of: [cyan]{user}[/cyan]\nExecuting [green]{name}[/green] api call...",
                    total=None,
                )

                dt_api = API(
                    user,
                    key,
                    app_name=cls.APP_PARTNER_NAME,
                    verify_ssl=verify_ssl,
                    rate_limit=rate_limit,
                    always_sign_api_key=always_sign_api_key,
                )
                dt_api_func = getattr(dt_api, name)

                params = params | kwargs

                response = dt_api_func(**params)
                progress.add_task(
                    description=f"Preparing results with format of {response_format}...",
                    total=None,
                )

                output = cls._get_formatted_output(cmd_name=name, response=response, out_format=response_format)

                if isinstance(out_file, _io.TextIOWrapper):
                    # use rich `print` command to prettify the ouput in sys.stdout
                    if response.product in FEEDS_PRODUCTS_LIST:
                        print(output)
                    else:
                        print(response)
                else:
                    # if it's a file then write
                    out_file.write(output if output.endswith("\n") else output + "\n")
                time.sleep(0.25)
        except Exception as e:
            if isinstance(e, ServiceException):
                code = typer.style(getattr(e, "code", 400), fg=typer.colors.BRIGHT_RED)
                _reason = getattr(e, "reason", {})
                # check data type first as some of the reasons is just plain text
                if isinstance(_reason, dict):
                    _reason = _reason.get("error", {}).get("message") or "Unknown Error occured."

                reason = typer.style(_reason, bg=typer.colors.RED)

                err_msg_format = f"Error occured while fetching data from the API: [{code}] Reason: {reason}"
                typer.echo(message=err_msg_format)
            else:
                typer.echo(message=e)
            return
