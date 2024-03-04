import time
import typer
import inspect
import shutil

from typing import List, Any, Optional, Callable
from typing_extensions import Annotated
from itertools import zip_longest

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
from typer.rich_utils import rich_format_help

from domaintools import API
from domaintools._version import current as version
from domaintools.cli_click import DTCommand, DTCommandArgs, DTCommandBuilder


class DTTyperClient:
    def make_commands(self, app: typer.Typer, dt_commands: List[DTCommand]):
        for dt_command in dt_commands:
            if dt_command.name == "iris_investigate":
                # TODO: right now the current doc in our api class doesn't print properly
                # need to re-write it here just to test.
                # I think we can just update the doc function itself on the API class.
                # or find a way to format the help-text without hard-coding it.
                dt_command.help = """
                    Returns back a list of domains based on the provided filters.
                    The following filters are available beyond what is parameterized as kwargs:

                    - ip: Search for domains having this IP.
                    - email: Search for domains with this email in their data.
                    - email_domain: Search for domains where the email address uses this domain.
                    - nameserver_host: Search for domains with this nameserver.
                    - nameserver_domain: Search for domains with a nameserver that has this domain.
                    - nameserver_ip: Search for domains with a nameserver on this IP.
                    - registrar: Search for domains with this registrar.
                    - registrant: Search for domains with this registrant name.
                    - registrant_org: Search for domains with this registrant organization.
                    - mailserver_host: Search for domains with this mailserver.
                    - mailserver_domain: Search for domains with a mailserver that has this domain.
                    - mailserver_ip: Search for domains with a mailserver on this IP.
                    - redirect_domain: Search for domains which redirect to this domain.
                    - ssl_hash: Search for domains which have an SSL certificate with this hash.
                    - ssl_subject: Search for domains which have an SSL certificate with this subject string.
                    - ssl_email: Search for domains which have an SSL certificate with this email in it.
                    - ssl_org: Search for domains which have an SSL certificate with this organization in it.
                    - google_analytics: Search for domains which have this Google Analytics code.
                    - adsense: Search for domains which have this AdSense code.
                    - tld: Filter by TLD. Must be combined with another parameter.
                    - search_hash: Use search hash from Iris to bring back domains.

                    You can loop over results of your investigation as if it was a native Python list:

                    for result in api.iris_investigate(ip='199.30.228.112'):  # Enables looping over all related results

                    api.iris_investigate(QUERY)['results_count'] Returns the number of results returned with this request
                    api.iris_investigate(QUERY)['total_count'] Returns the number of results available within Iris
                    api.iris_investigate(QUERY)['missing_domains'] Returns any domains that we were unable to find
                    api.iris_investigate(QUERY)['limit_exceeded'] Returns True if you've exceeded your API usage
                    api.iris_investigate(QUERY)['position'] Returns the position key that can be used to retrieve the next page:
                    next_page = api.iris_investigate(QUERY, position=api.iris_investigate(QUERY)['position'])
                """

            def create_dt_api_command(dt_command: DTCommand):
                @app.command(name=dt_command.name, help=dt_command.help)
                def dt_api_command(
                    domains: Annotated[
                        str, typer.Option("--domains", help="domain_to_query")
                    ],
                    user: Annotated[
                        str, typer.Option("--user", help="DomainTools API username")
                    ],
                    key: Annotated[
                        str, typer.Option("--key", help="DomainTools API key")
                    ],
                ):
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        transient=True,
                    ) as progress:
                        progress.add_task(
                            description=f"Executing [green]{dt_command.name}[/green] api call...",
                            total=0,
                        )
                        params = {"domains": domains}
                        api = API(
                            user,
                            key,
                            app_name="python_wrapper_cli_v2",
                            verify_ssl=False,
                        )
                        response = getattr(api, dt_command.name)(**params)
                        if response:
                            progress.add_task(
                                description="Preparing results...",
                                total=0,
                            )
                            time.sleep(1)

                        print(response)
                        print(f"Done fetching results from {dt_command.name}.")

                return dt_api_command

            create_dt_api_command(dt_command)


def run():
    app = typer.Typer()

    # build domaintools commandline tools via our Domaintools API class
    commands = DTCommandBuilder.build()
    typer_client = DTTyperClient()
    typer_client.make_commands(app, commands)

    # start the cli app
    app()
