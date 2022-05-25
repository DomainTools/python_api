"""Tests the CLI interface for DomainTools APIs"""
import pytest
from domaintools import __version__, cli


def test_domain_search():
    (out_file, out_format, arguments) = cli.parse(['domain_search', 'google', '--anchor-right', 'true'])
    assert out_format == 'json'
    assert arguments['api_call'] == 'domain_search'
    assert arguments['query'] == 'google'
    assert arguments['anchor_right'] == 'true'


def test_iris_investigate():
    (out_file, out_format, arguments) = cli.parse(['iris_investigate', '--domains', 'domaintools.com'])
    assert out_format == 'json'
    assert arguments['api_call'] == 'iris_investigate'
    assert arguments['domains'] == 'domaintools.com'


def test_iris_investigate_search_hash():
    (out_file, out_format, arguments) = cli.parse(['iris_investigate', '--search-hash', 'U2FsdGVkX19G/DWIwCQN8p2e/pbIvv5yRwbZs1vas8BrvEaohzKi5FbgAXPB+souItygalew9jxEpeNvmDNfVD0IuKPknPO5zQA9Eic38zpSpRVPQ9P2jhBpZJkMfseS5VVoM4BSL2lmGAhX0RPpZ8PMXSUtRP8IJUDo8n4HIi0r/+/vD5yIUSdRujA4sXIPpLujjW80PKJkyrFWmT35Y6aYxdlw6U05tBcc1k9ThnVNWL8K/R41OeSrFuTSrmTpCrOTF5YvCcZakbRp+BZUH76k8yTY+mU1HhCsT54fgPY0YsCcvXt2x8y89HXlCAio8Gz+nxLU2YeWaxAsvnNpyqm2WQZPrlXzFTxtbymN8QzVRBwGHxJcqixcW43FlsjA1FIAu6dJ/zS3ibxf9aFqspibOngLc2dufcHRclMXg1i2AmTF6fTM23oLT3GVSc7JwYycRwn94xbC4eQDzkzVQiU/60mVMEIKegTPByoYBJU='])
    assert out_format == 'json'
    assert arguments['api_call'] == 'iris_investigate'
    assert arguments['search_hash'] == 'U2FsdGVkX19G/DWIwCQN8p2e/pbIvv5yRwbZs1vas8BrvEaohzKi5FbgAXPB+souItygalew9jxEpeNvmDNfVD0IuKPknPO5zQA9Eic38zpSpRVPQ9P2jhBpZJkMfseS5VVoM4BSL2lmGAhX0RPpZ8PMXSUtRP8IJUDo8n4HIi0r/+/vD5yIUSdRujA4sXIPpLujjW80PKJkyrFWmT35Y6aYxdlw6U05tBcc1k9ThnVNWL8K/R41OeSrFuTSrmTpCrOTF5YvCcZakbRp+BZUH76k8yTY+mU1HhCsT54fgPY0YsCcvXt2x8y89HXlCAio8Gz+nxLU2YeWaxAsvnNpyqm2WQZPrlXzFTxtbymN8QzVRBwGHxJcqixcW43FlsjA1FIAu6dJ/zS3ibxf9aFqspibOngLc2dufcHRclMXg1i2AmTF6fTM23oLT3GVSc7JwYycRwn94xbC4eQDzkzVQiU/60mVMEIKegTPByoYBJU='


def test_not_authenticated():
    (out_file, out_format, arguments) = cli.parse(args=['-c', 'non-existent', 'domain_search', 'google',
                                                        '--max-length', '100'])
    assert out_format == 'json'
    assert not arguments.get('user')
    assert not arguments.get('key')


def test_stream_in():
    with pytest.raises((OSError, IOError)):
        cli.parse(['domain_search', 'google', '--max-length', '-'])
