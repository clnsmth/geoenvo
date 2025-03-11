"""geoenvo"""

import sys
from importlib.metadata import version
import daiquiri


__version__ = version("geoenvo")

# Set up logging globally
daiquiri.setup(level=daiquiri.logging.DEBUG)
logger = daiquiri.getLogger("geoenvo")


def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handles all uncaught exceptions and logs them globally."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow user to exit with Ctrl+C without logging as an error
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical(
        f"Unhandled exception occurred: {exc_value}",
        exc_info=(exc_type, exc_value, exc_traceback),
    )


# Set global exception handler
sys.excepthook = global_exception_handler

logger.info("geoenvo package initialized with global exception logging.")
