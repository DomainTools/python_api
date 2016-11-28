"""Defines all test wide settings and variables"""
from os import environ

from domaintools import API
from vcr import VCR


def remove_server(response):
    response.get('headers', {}).pop('server', None)
    return response


vcr = VCR(before_record_response=remove_server, filter_query_parameters=['api_key', 'api_username'],
          cassette_library_dir='tests/fixtures/vcr/', path_transformer=VCR.ensure_suffix('.yaml'),
          record_mode='new_episodes')
with vcr.use_cassette('init_user_account'):
    api = API(environ.get('TEST_USER', 'test_user'), environ.get('TEST_KEY', 'test_key'))
