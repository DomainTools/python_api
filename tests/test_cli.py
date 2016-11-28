"""Tests the CLI interface for DomainTools' APIs"""
import pytest
from domaintools import __version__, cli


def test_domain_search():
    (out_file, out_format, arguments) = cli.parse(['domain_search', 'google', '--anchor-right', 'true'])
    assert out_format == 'json'
    assert arguments['api_call'] == 'domain_search'
    assert arguments['query'] == 'google'
    assert arguments['anchor_right'] == 'true'


def test_not_authenticated():
    (out_file, out_format, arguments) = cli.parse(args=['-c', 'non-existent', 'domain_search', 'google',
                                                        '--max-length', '100'])
    assert out_format == 'json'
    assert not arguments.get('user', None)
    assert not arguments.get('key', None)


def test_stream_in():
    with pytest.raises((OSError, IOError)):
        cli.parse(['domain_search', 'google', '--max-length', '-'])
