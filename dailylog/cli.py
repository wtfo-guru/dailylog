"""Top-level module cli for dailylog."""

import sys
import types
from pathlib import Path
from typing import AnyStr, NoReturn, Optional

import click
from click.core import Context
from wtforglib.files import ensure_directory

from dailylog.cache import CONST_HOUR, Cache
from dailylog.config import Config
from dailylog.version import VERSION

CONTEXT_SETTINGS = types.MappingProxyType({"help_option_names": ["-h", "--help"]})


def print_version(ctx: Context, _aparam: AnyStr, avalue: AnyStr) -> None:
    """Print package version and exits.

    Parameters
    ----------
    ctx : Context
        click context object
    _aparam : AnyStr
        dunno
    avalue : AnyStr
        dunno
    """
    if not avalue or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.command()
@click.option("key", "-k", type=str, required=True, help="Specify key")
@click.option("message", "-m", type=str, required=True, help="Specify message")
@click.option(
    "log_fn",
    "-l",
    type=str,
    required=False,
    help="Specify alternate log file",
)
@click.pass_context
def error(ctx: Context, key: str, message: str, log_fn: Optional[str]) -> NoReturn:
    """Log an error."""
    cache = Cache(ctx)
    cache.error(key, message, log_fn)
    sys.exit(0)


@click.command()
@click.option("key", "-k", type=str, required=True, help="Specify key")
@click.option("message", "-m", type=str, required=True, help="Specify message")
@click.option(
    "suppress",
    "-s",
    type=int,
    default=CONST_HOUR,
    help="Specify seconds to suppress (default 86400 [one day])",
)
@click.option(
    "log_fn",
    "-l",
    type=str,
    required=False,
    help="Specify alternate log file",
)
@click.pass_context
def warning(ctx: Context, key: str, message: str, suppress: int, log_fn: Optional[str]) -> NoReturn:
    """Log a warning."""
    cache = Cache(ctx)
    if log_fn is None:
        cache.log(key, message, label="WARNING", suppress=suppress)
    else:
        cache.log(key, message, label="WARNING", suppress=suppress)
    sys.exit(0)


@click.command()
@click.argument("log_fn", type=str, required=True, nargs=1)
@click.pass_context
def set_default_log(ctx: Context, log_fn: str) -> NoReturn:
    """Set a new default log."""
    config = Config(ctx)
    config.set_default_log(log_fn)
    if config.is_test():
        # For coverage purposes
        config.is_verbose()
    sys.exit(0)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-C",
    "--cache",
    required=False,
    type=str,
    help="specify alternate cache file",
)
@click.option(
    "-c",
    "--config",
    required=False,
    type=str,
    help="specify alternate config file",
)
@click.option("-d", "--debug", count=True, default=0, help="increment debug level")
@click.option("-t", "--test/--no-test", default=False, help="specify test mode")
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="increment verbosity level",
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    expose_value=False,
    callback=print_version,
    is_eager=True,
    help="show version and exit",
)
@click.pass_context
def main(ctx, cache, config, debug, test, verbose):
    """Entry point for click script."""
    ctx.ensure_object(dict)
    if cache is None:
        path = Path.home() / ".cache"
        ensure_directory(path)
        cache = str(path / "dailylog.json")
    if config is None:
        path = Path.home() / ".config"
        ensure_directory(path)
        config = str(path / "dailylog.yaml")
    ctx.obj["debug"] = debug
    ctx.obj["test"] = test
    ctx.obj["verbose"] = verbose
    ctx.obj["cache"] = cache
    ctx.obj["config"] = config


main.add_command(error)
main.add_command(warning)
main.add_command(set_default_log)

if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma no cover
# vim:ft=py noqa: E800
