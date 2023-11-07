"""Test level module test_cli for dailylog."""

import time

from wtforglib.files import load_json_file

from dailylog.cache import CONST_CACHE_VERSION
from dailylog.cli import main

# CONST_ARG_SET_DEFAULT_LOG = "set-default-log"
# CONST_OPT_LOWER_C = "-c"
# # TODO: make windoze compatible consts
# CONST_TEST_CONFIG = "/tmp/daily.yaml"
CONST_TEST_CACHE = "/tmp/daily.cache"
CONST_KEY_TEST = "test"
# CONST_TEST_LOG = "/tmp/daily.log"
# CONST_TEST_CONFIG_CONTENT = """---
# version: 1
# default_log: /home/superman/dailylog
# ...
# """


def test_cli_cache_debug(cli_runner, fs, printer, capsys):
    """Test cli set-default-log."""
    # noinspection PyTypeChecker
    test_result = cli_runner.invoke(
        main,
        [
            "-C",
            CONST_TEST_CACHE,
            "log",
            "-k",
            CONST_KEY_TEST,
            "-m",
            "Don't eat yellow snow",
        ],
    )
    time.sleep(1)
    test_result = cli_runner.invoke(
        main,
        [
            "-C",
            CONST_TEST_CACHE,
            "log",
            "-k",
            CONST_KEY_TEST,
            "-m",
            "Don't eat yellow snow",
        ],
    )
    assert not test_result.exception
    assert test_result.exit_code == 0
    json_result = load_json_file(CONST_TEST_CACHE)
    printer(str(json_result))
    out, err = capsys.readouterr()
    printer("sysout: {0}".format(out))
    printer("syserr: {0}".format(err))
    assert json_result["version"] == CONST_CACHE_VERSION
    assert json_result["entries"][CONST_KEY_TEST]["suppressed"] == 1
    # with open(CONST_TEST_CONFIG, "r") as fd:
    #     yaml_result = yaml.safe_load(fd)
    # assert yaml_result.get("default_log") == CONST_TEST_LOG
    # assert yaml_result.get("version") == CURRENT_CONFIG_VERSION
