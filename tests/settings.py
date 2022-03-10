"""Defines all test wide settings and variables"""
from os import environ
from yarl import URL

from domaintools import API, utils
from vcr import VCR


def remove_server(response):
    response.get('headers', {}).pop('server', None)
    if 'url' in response:
        url = URL(response['url'])
        query = dict(url.query)
        if 'api_username' in query:
            query.update(api_username='test')
        if 'api_key' in query:
            query.update(api_key='test')
        if 'signature' in query:
            query.update(signature='test')
        response['url'] = str(url.with_query(query))
    return response


vcr = VCR(before_record_response=remove_server, filter_query_parameters=['timestamp', 'signature', 'api_username', 'api_key'], filter_post_data_parameters=['timestamp', 'signature', 'api_username', 'api_key'],
          cassette_library_dir='tests/fixtures/vcr/', path_transformer=VCR.ensure_suffix('.yaml'),
          record_mode='new_episodes')
with vcr.use_cassette('init_user_account'):
    api = API(environ.get('TEST_USER', 'test'), environ.get('TEST_KEY', 'test'), always_sign_api_key=True)
