"""Defines how to interact with the domaintools API via the command line"""
import argparse
import inspect
import os.path
import sys

from domaintools import API
from domaintools._version import current as version

try: # pragma: no cover
    from itertools import zip_longest
except ImportError: # pragma: no cover
    from itertools import izip_longest as zip_longest

API_CALLS = tuple((api_call for api_call in dir(API) if not api_call.startswith('_') and
                   callable(getattr(API, api_call, None))))


def parse(args=None):
    """Defines how to parse CLI arguments for the DomainTools API"""
    parser = argparse.ArgumentParser(description='The DomainTools CLI API Client')
    parser.add_argument('-u', '--username', dest='user', default='', help='API Username')
    parser.add_argument('-k', '--key', dest='key', default='', help='API Key')
    parser.add_argument('-c', '--credfile', dest='credentials', default=os.path.expanduser('~/.dtapi'),
                        help='Optional file with API username and API key, one per line.')
    parser.add_argument('-l', '--rate-limit', dest='rate_limit', action='store_true', default=False,
                        help='Rate limit API calls against the API based on per minute limits.')
    parser.add_argument('-f', '--format', dest='format', choices=['list', 'json','xml','html'], default='json')
    parser.add_argument('-o', '--outfile', dest='out_file', type=argparse.FileType('wbU'), default=sys.stdout,
                        help='Output file (defaults to stdout)')
    parser.add_argument('-v', '--version', action='version', version='DomainTools CLI API Client {0}'.format(version))
    parser.add_argument('--no-https', dest='https', action='store_false', default=True,
                        help='Use HTTP instead of HTTPS.')
    parser.add_argument('--no-verify-ssl', dest='verify_ssl', action='store_false', default=True,
                        help='Skip verification of SSL certificate when making HTTPs API calls')

    subparsers = parser.add_subparsers(help='The name of the API call you wish to perform (`whois` for example)',
                                       dest='api_call')
    subparsers.required = True
    for api_call in API_CALLS:
        api_method = getattr(API, api_call)
        subparser = subparsers.add_parser(api_call, help=api_method.__name__)
        spec = inspect.getargspec(api_method)

        for argument_name, default in reversed(list(zip_longest(reversed(spec.args or []),
                                                                reversed(spec.defaults or []), fillvalue='EMPTY'))):
            if argument_name == 'self':
                continue
            elif default == 'EMPTY':
                subparser.add_argument(argument_name)
            else:
                subparser.add_argument('--{0}'.format(argument_name.replace('_', '-')), dest=argument_name,
                                       default=default, nargs='*')

    arguments = vars(parser.parse_args(args) if args else parser.parse_args())
    if not arguments.get('user', None) or not arguments.get('key', None):
        try:
            with open(arguments.pop('credentials')) as credentials:
                arguments['user'], arguments['key'] = credentials.readline().strip(), credentials.readline().strip()
        except Exception:
            pass

    for key, value in arguments.items():
        if value in ('-', ['-']):
            arguments[key] == (line.strip() for line in sys.stdin.readlines())
        elif value == []:
            arguments[key] = True
        elif type(value) == list and len(value) == 1:
            arguments[key] = value[0]

    return (arguments.pop('out_file'), arguments.pop('format'), arguments)


def run(): # pragma: no cover
    """Defines how to start the CLI for the DomainTools API"""
    out_file, out_format, arguments = parse()
    user, key = arguments.pop('user', None), arguments.pop('key', None)
    if not user or not key:
        sys.stderr.write('Credentials are required to perform API calls.\n')
        sys.exit(1)

    api = API(user, key, https=arguments.pop('https'), verify_ssl=arguments.pop('verify_ssl'),
              rate_limit=arguments.pop('rate_limit'))
    response = getattr(api, arguments.pop('api_call'))(**arguments)
    output = str(getattr(response, out_format) if out_format != 'list' else response.as_list())
    out_file.write(output if output.endswith('\n') else output + '\n')
