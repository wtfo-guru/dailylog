"""Top level module for dailylog."""

from click.core import Context
from pathlib import Path

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


