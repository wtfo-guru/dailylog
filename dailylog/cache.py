"""Top level module cache for dailylog."""

from pathlib import Path
from typing import Optional

import click
from click.core import Context
from wtforglib.files import load_json_file, write_json_file
from wtforglib.kinds import StrAnyDict

from dailylog.options import Options


class Cache(Options):
    """Class to manage the cache."""

    cache: StrAnyDict

    def __init__(self, ctx: Context):
        """Constructor for cache class."""
        super().__init__(ctx)
        self._load_cache()

    def warning(self, key: str, message: str, log_fn: Optional[str] = None) -> None:
        """Log message as warning.

        Args:
            key (str): unique key for warning
            message (str): the message to log
            log_fn (Optional[str], optional): alternate log file. Defaults to None.
        """
        self._log(key, "WARN", message, log_fn)

    def error(self, key: str, message: str, log_fn: Optional[str] = None) -> None:
        """Log message as error.

        Args:
            key (str): unique key for error
            message (str): the message to log
            log_fn (Optional[str], optional): alternate log file. Defaults to None.
        """
        self._log(key, "ERROR", message, log_fn)

    def _log(
        self,
        key: str,
        label: str,
        message: str,
        log_fn: Optional[str] = None,
    ) -> None:
        """Log message.

        Args:
            key (str): unique key for entry
            label (str): level label
            message (str): the message to log
            log_fn (Optional[str], optional): alternate log file. Defaults to None.
        """
        click.echo("{0}: {1}".format(label, message))

    def _load_cache(self) -> None:
        """Load case from file it exist otherwise create a cache."""
        cache_path = self.cache_path()
        if cache_path.is_file():
            self.cache = load_json_file(cache_path)
        else:
            self.cache = {}
            self.cache["version"] = 1
            self.cache["default_log"] = str(Path().home() / "daily.log")
            self._save_cache()

    def _save_cache(self) -> None:
        """Load cacheuration from file."""
        write_json_file(self.cache_path(), self.cache)
