"""Test level module test_cli for dailylog."""
import re

from dailylog.cli import main


def test_cli(cli_runner):
    """Test cli help text."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main)
    assert test_result.exit_code == 0
    assert not test_result.exception
    for regex in "hello":
        assert re.search(regex, test_result.output)


def test_cli_with_option(cli_runner, version):
    """Test cli version option."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main, ["--version"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert test_result.output.strip() == version


def test_cli_hello(cli_runner):
    """Test cli version option."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main, ["hello"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert test_result.output.strip() == "Hello World"


def test_cli_hello_option(cli_runner):
    """Test cli version option."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main, ["hello", "cowboy"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert test_result.output.strip() == "Hello Cowboy"
