# -*- coding: utf-8 -*-
"""
utils.py
========
Helper functions: logging configuration and privilege checks.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import NoReturn


def setup_logging(level: int = logging.INFO) -> None:
    """Configure a console logger with a clean format."""
    root = logging.getLogger()
    if root.handlers:
        return  # already configured
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)-18s | %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    root.addHandler(handler)


def check_privileges() -> None:
    """Verify the script has the privileges required for global hotkeys.

    On Windows, registering global hotkeys through the `keyboard` package
    typically requires the process to run as Administrator. This helper
    prints a friendly warning if that is not the case, but does not abort
    execution so the script remains usable for testing.
    """
    if os.name == "nt":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_admin = False
        if not is_admin:
            logging.getLogger("utils").warning(
                "Running without administrator privileges - "
                "global hotkeys may not register correctly."
            )
    else:
        logging.getLogger("utils").info(
            "Non-Windows platform detected - some features may be unavailable."
        )


def fail_fast(message: str) -> NoReturn:
    """Log an error and exit with a non-zero status code."""
    logging.getLogger("utils").error(message)
    sys.exit(1)
