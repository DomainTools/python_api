"""Tests the CLI interface for DomainTool's APIs"""
import pytest

from domaintools import cli, __version__
from tests.settings import vcr, api


@vcr.use_cassette
def test_version(capsys):
    with pytest.raises(SystemExit):
        cli.run(api, ['-v'])
    out, err = capsys.readouterr()
    assert __version__ in out or __version__ in err


@vcr.use_cassette
def test_help(capsys):
    with pytest.raises(SystemExit):
        cli.run(api, ['--help'])
    out, err = capsys.readouterr()
    assert 'DomainTools' in out


@vcr.use_cassette
def test_domain_search(capsys):
    cli.run(api, ['domain_search', 'google', '--anchor-right', 'true'])
    out, err = capsys.readouterr()
    assert 'google' in out and 'com' in out


@vcr.use_cassette
def test_not_authenticated(capsys):
    with pytest.raises(SystemExit):
        cli.run(args=['-c', 'non-existent', 'domain_search', 'google', '--max-length', '100'])

    out, err = capsys.readouterr()
    assert 'Credentials are required' in err


@vcr.use_cassette
def test_stream_in(capsys):
    with pytest.raises(OSError):
        cli.run(args=['domain_search', 'google', '--max-length', '-'])
