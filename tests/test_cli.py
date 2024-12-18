"""Tests the CLI interface for DomainTools APIs"""

import pytest
import os

from typer.testing import CliRunner

from domaintools.cli import dt_cli
from domaintools._version import current

runner = CliRunner()


def test_match_cli_version():
    result = runner.invoke(dt_cli, ["--version"])

    expected_res = f"DomainTools CLI API Client {current}"
    assert expected_res == result.stdout.strip()


def test_valid_command():
    user = os.environ.get("TEST_USER", "test")
    key = os.environ.get("TEST_KEY", "key")
    result = runner.invoke(dt_cli, ["account_information", "--help"])
    assert "Provides a snapshot of your accounts current API usage." in result.stdout


def test_invalid_command():
    result = runner.invoke(dt_cli, ["test_invalid_command"])
    assert "No such command 'test_invalid_command'." in result.stdout


def test_no_creds_file_not_found():
    result = runner.invoke(dt_cli, ["iris_investigate", "--domain", "domaintools.com"])
    assert "No such file or directory" in result.stdout
