import inspect
import shutil
import argparse
import rich_click as click

from typing import List, Any, Optional, Callable
from itertools import zip_longest

from domaintools import API
from domaintools._version import current as version


class DTCommandArgs:
    def __init__(
        self, name: str, default: Optional[str] = None, arg_type: Optional[Any] = None
    ):
        self.name = name
        self.arg_type = arg_type
        self.default = default

    def __repr__(self):
        return f"{self.name}"


class DTCommand:
    def __init__(
        self,
        name: str,
        func: Callable,
        arguments: List[DTCommandArgs],
        help_text: str = "",
        description: str = "",
    ):
        self.name = name
        self.func = func
        self.arguments = arguments
        self.help = help_text
        self.description = description

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.name} - Function: {self.func.__name__} - Arguments: {self.arguments}"


class DTCommandBuilder:
    @classmethod
    def get_api_calls(cls):
        return tuple(
            (
                api_call
                for api_call in dir(API)
                if not api_call.startswith("_")
                and callable(getattr(API, api_call, None))
            )
        )

    @classmethod
    def build(cls) -> List[DTCommand]:
        list_of_commands = []
        dt_api_calls = cls.get_api_calls()
        for api_call in dt_api_calls:
            api_method = getattr(API, api_call)
            help_text = inspect.getdoc(api_method)
            description = inspect.getdoc(api_method)

            spec = inspect.getfullargspec(api_method)

            list_of_arguments = []
            for argument_name, default in reversed(
                list(
                    zip_longest(
                        reversed(spec.args or []),
                        reversed(spec.defaults or []),
                        fillvalue="EMPTY",
                    )
                )
            ):
                if argument_name == "self":
                    continue

                if default == "EMPTY":
                    command_arg = DTCommandArgs(argument_name)
                else:
                    command_arg = DTCommandArgs(
                        name="--{0}".format(argument_name.replace("_", "-")),
                        default=default,
                    )
                list_of_arguments.append(command_arg)

            list_of_commands.append(
                DTCommand(
                    name=api_call,
                    func=api_method,
                    arguments=list_of_arguments,
                    help_text=help_text,
                    description=description,
                )
            )

        return list_of_commands


class DTClickClient:
    available_commands = []

    @staticmethod
    @click.group(
        context_settings={
            "max_content_width": shutil.get_terminal_size().columns - 10,
            "help_option_names": ["-h", "--help"],
        }
    )
    @click.option("-v", "--verbose", is_flag=True, help="Run in verbose mode.")
    def build_group(verbose):
        if verbose:
            click.echo("running in verbose mode")

    def make_commands(self, dt_commands: List[DTCommand]):
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
                @click.command(
                    name=dt_command.name,
                    help=dt_command.help,
                    context_settings={
                        "max_content_width": shutil.get_terminal_size().columns - 10,
                        "help_option_names": ["-h", "--help"],
                    },
                )
                @click.rich_config(
                    help_config=click.RichHelpConfiguration(use_markdown=True)
                )
                # TODO: arguments can be loop as well but for the purpose of spike
                # this is hardcoded for the meantime
                @click.option("-d", "--domains", help="domain to query", required=True)
                @click.option(
                    "-u", "--user", help="DomainTools API username", required=True
                )
                @click.option("-k", "--key", help="DomainTools API Key", required=True)
                def dt_api_command(domains, user, key):
                    params = {"domains": domains}
                    click.echo(f"Executing {dt_command.name} command...")
                    api = API(
                        user,
                        key,
                        app_name="python_wrapper_cli_v2",
                        verify_ssl=False,
                    )
                    response = getattr(api, dt_command.name)(**params)
                    print(response)

                return dt_api_command

            self.build_group.add_command(create_dt_api_command(dt_command))


def run():
    commands = DTCommandBuilder.build()
    click_client = DTClickClient()
    click_client.make_commands(commands)
    click_client.build_group()
