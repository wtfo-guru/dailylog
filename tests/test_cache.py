"""Test level module test_cli for dailylog."""

import json

from dailylog.cache import CURRENT_CACHE_VERSION
from dailylog.cli import main

# CONST_ARG_SET_DEFAULT_LOG = "set-default-log"
# CONST_OPT_LOWER_C = "-c"
# # TODO: make windoze compatible consts
# CONST_TEST_CONFIG = "/tmp/daily.yaml"
# CONST_TEST_CACHE = "/tmp/daily.cache"
# CONST_TEST_LOG = "/tmp/daily.log"
# CONST_TEST_CONFIG_CONTENT = """---
# version: 1
# default_log: /home/superman/dailylog
# ...
# """


def test_cli_cache_warning(cli_runner, fs):
    """Test cli set-default-log."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(main, ["warning", "Don't eat yellow snow"])
    assert not test_result.exception
    assert test_result.exit_code == 0
    # with open(CONST_TEST_CONFIG, "r") as fd:
    #     yaml_result = yaml.safe_load(fd)
    # assert yaml_result.get("default_log") == CONST_TEST_LOG
    # assert yaml_result.get("version") == CURRENT_CONFIG_VERSION
