"""Defines all test wide settings and variables"""
from os import environ

from domaintools import API
from vcr import VCR


def remove_server(response):
    response.get('headers', {}).pop('server', None)
    if 'url' in response:
        response['url'] = response['url'].update_query(api_username='test', api_key='test')
    return response


vcr = VCR(before_record_response=remove_server, filter_query_parameters=['timestamp', 'signature', 'api_username'], filter_post_data_parameters=['timestamp', 'signature', 'api_username'],
          cassette_library_dir='tests/fixtures/vcr/', path_transformer=VCR.ensure_suffix('.yaml'),
          record_mode='new_episodes')
with vcr.use_cassette('init_user_account'):
    api = API(environ.get('TEST_USER', 'test'), environ.get('TEST_KEY', 'test'), always_sign_api_key=True)
