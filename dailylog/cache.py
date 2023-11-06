"""Top level module cache for dailylog."""

import sys
from typing import Optional

import click
from click.core import Context
from wtforglib.files import load_json_file, write_json_file
from wtforglib.kinds import StrAnyDict

from dailylog.config import Config

CONST_CACHE_VERSION = 1
CONST_HOUR = 86400

class Cache(Config):
    """Class to manage the cache."""

    cache: StrAnyDict

    def __init__(self, ctx: Context):
        """Constructor for cache class."""
        super().__init__(ctx)
        self._load_cache()

    def log_message(self, key: str, message: str, **kwargs) -> None:
        """Log message.

        Args:
            key (str): unique key for warning
            message (str): the message to log
            log_fn (Optional[str], optional): alternate log file. Defaults to None.

        Other Parameters
        ----------------
        label_kwarg: str
            Should be either WARNING or ERROR
        suppress_kwarg: int
            This is an integer representing number of seconds to suppress screen output
        logfn_kwarg: str
            this is a string representing a log file other than the default
        **kwargs : dict
            Other infrequently used keyword arguments.
        """
        label = kwargs.get("label", "ERROR")
        log_fn = kwargs.get("logfn", self._default_log())
        suppress = kwargs.get("suppress", CONST_HOUR)
        if key in self.cache["entries"]:
            record = self.cache["entries"][key]
            shown = record.get("shown", False)
        sys.stderr.write("{0}:\n".format(label))


    def _load_cache(self) -> None:
        """Load case from file it exist otherwise create a cache."""
        cache_path = self.cache_path()
        if cache_path.is_file():
            self.cache = load_json_file(cache_path)
        else:
            self.cache = {}
            self.cache["version"] = CONST_CACHE_VERSION
            self.cache["entries"] = {}
            self._save_cache()

    def _save_cache(self) -> None:
        """Load cacheuration from file."""
        write_json_file(self.cache_path(), self.cache)
