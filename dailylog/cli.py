"""Top-level module cli for dailylog."""

import sys
import types
from typing import AnyStr, NoReturn

import click
from click.core import Context

from dailylog.version import VERSION

CONTEXT_SETTINGS = types.MappingProxyType({"help_option_names": ["-h", "--help"]})


def print_version(ctx: Context, aparam: AnyStr, avalue: AnyStr) -> None:
    """Prints package version and exits.

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
@click.argument("who", type=str, required=True, nargs=1)
@click.pass_context
def hello(ctx: Context, who: str = "world") -> NoReturn:
    """Print hello who."""
    click.echo("Hello {0}".format(who.capitalize()))
    sys.exit(0)


@click.group(context_settings=CONTEXT_SETTINGS)
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
def main(ctx, debug, test, verbose):
    """Provides single interface to several common Linux package managers."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["test"] = test
    ctx.obj["verbose"] = verbose


main.add_command(hello)

if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma no cover
# vim:ft=py noqa: E800
