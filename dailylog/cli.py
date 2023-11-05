"""Top-level module cli for dailylog."""

import sys
import types
from typing import AnyStr, NoReturn, Optional

import click
from click.core import Context

from dailylog.version import VERSION
from dailylog.config import Config

CONTEXT_SETTINGS = types.MappingProxyType({"help_option_names": ["-h", "--help"]})


def print_version(ctx: Context, _aparam: AnyStr, avalue: AnyStr) -> None:
    """Print package version and exits.

    Parameters
    ----------
    ctx : Context
        click context object
    aparam : AnyStr
        dunno
    avalue : AnyStr
        dunno
    """
    if not avalue or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.command()
@click.argument("log_fn", type=str, required=True, nargs=1)
@click.pass_context
def set_default_log(ctx: Context, logfn: str) -> NoReturn:
    """Print hello who."""
    config = Config(ctx)
    config.set_default_log(log_fn)
    sys.exit(0)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-c", "--config", required=False, type=str, help="specify alternate config file")
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
def main(ctx, config, debug, test, verbose):
    """Entry point for click script."""
    if config is None:
        config = str(Path.home() / ".config" / "dailylog")
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["test"] = test
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = config


main.add_command(set_default_log)

if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma no cover
# vim:ft=py noqa: E800
