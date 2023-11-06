"""Test level module test_cli for dailylog."""
import re

import yaml

from dailylog.cli import main
from dailylog.config import CURRENT_CONFIG_VERSION

CONST_ARG_SET_DEFAULT_LOG = "set-default-log"
CONST_OPT_LOWER_C = "-c"
# TODO: make windoze compatible consts
CONST_TEST_CONFIG = "/tmp/daily.yaml"
CONST_TEST_CACHE = "/tmp/daily.cache"
CONST_TEST_LOG = "/tmp/daily.log"
CONST_TEST_CONFIG_CONTENT = """---
version: 1
default_log: /home/superman/dailylog
...
"""


def test_cli(cli_runner):
    """Test cli help text."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main)
    assert test_result.exit_code == 0
    assert not test_result.exception
    for regex in ("warning", "error", CONST_ARG_SET_DEFAULT_LOG):
        assert re.search(regex, test_result.output)


def test_cli_with_option(cli_runner, version):
    """Test cli version option."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main, ["--version"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    assert test_result.output.strip() == version


def test_cli_set_default_log_missing_arg(cli_runner, fs):
    """Test cli missing arg."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main, [CONST_ARG_SET_DEFAULT_LOG])
    assert test_result.exception
    assert test_result.exit_code == 2


def test_cli_set_default_log(cli_runner, fs):
    """Test cli set-default-log."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(
        main,
        [
            "-t",
            "-d",
            CONST_OPT_LOWER_C,
            CONST_TEST_CONFIG,
            CONST_ARG_SET_DEFAULT_LOG,
            CONST_TEST_LOG,
        ],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    with open(CONST_TEST_CONFIG, "r") as fd:
        yaml_result = yaml.safe_load(fd)
    assert yaml_result.get("default_log") == CONST_TEST_LOG
    assert yaml_result.get("version") == CURRENT_CONFIG_VERSION


def test_cli_existing_config(cli_runner, fs):
    """Test cli set-default-log with existing config file."""
    fs.create_file(CONST_TEST_CONFIG, contents=CONST_TEST_CONFIG_CONTENT)
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(
        main,
        [
            CONST_OPT_LOWER_C,
            CONST_TEST_CONFIG,
            CONST_ARG_SET_DEFAULT_LOG,
            CONST_TEST_LOG,
        ],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    with open(CONST_TEST_CONFIG, "r") as fd:
        yaml_result = yaml.safe_load(fd)
    assert yaml_result.get("default_log") == CONST_TEST_LOG
    assert yaml_result.get("version") == CURRENT_CONFIG_VERSION


def test_cli_set_default_log_empty_str(cli_runner, fs):
    """Test cli set-default-log."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(
        main,
        [CONST_OPT_LOWER_C, CONST_TEST_CONFIG, CONST_ARG_SET_DEFAULT_LOG, ""],
    )
    assert test_result.exception
    assert test_result.exit_code == 1


def test_cli_set_default_log_relative(cli_runner, fs):
    """Test cli set-default-log."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(
        main,
        [
            CONST_OPT_LOWER_C,
            CONST_TEST_CONFIG,
            CONST_ARG_SET_DEFAULT_LOG,
            "where/am/i.log",
        ],
    )
    assert test_result.exception
    assert test_result.exit_code == 1
