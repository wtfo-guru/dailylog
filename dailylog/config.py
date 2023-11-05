"""Top level module for dailylog."""

import os

from click.core import Context
from pathlib import Path
from dailylog.exceptions import FilePermError

class Config:
    """Class to manage the configuration."""
    config_fn: Path

    def __init__(self, ctx: Context):
        """Constructor for Config class."""
        self.config_fn = Path(ctx.obj.get("config", ""))
        if not str(self.config_fn):
            raise ValueError("config path name cannot be empty")
        if not self.config_fn.is_absolute():
            raise ValueError("config path name must be absolute")
        if self.config_fn .is_file():
            self.config = self._load_config()
        else:
            self.config = {}
            self.config["version"] = 1
            self.default_log = Path().home() / "daily.log"
            self._save_config()

    def set_default_log(self, log_fn: str):
        """_summary_

        Parameters
        ----------
        log_fn : str
            _description_

        Raises
        ------
        FileNotFoundError
            _description_
        FilePermError
            _description_
        """
        log_path = Path(log_fn)
        if log_path.exists():
            if not log_path.is_file():
                raise FileNotFoundError("Not a file: {0}".format(log_path))
            if not c:
                raise FilePermError("Not writable: {0}".format(log_path))
        elif not log_path.parent.is_dir():
            raise FileNotFoundError("Directory not found: {0}".format(log_path.parent))
        elif not log_path.parent.is_dir():
            raise FileNotFoundError("Not a directory: {0}".format(log_path.parent))
        elif not os.access(log_path.parent, os.W_OK):
            raise FilePermError("Not writable: {0}".format(log_path.parent))


