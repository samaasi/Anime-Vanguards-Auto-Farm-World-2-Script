# -*- coding: utf-8 -*-
"""
main.py
=======
Entry point for the Anime Vanguards Auto Farm World 2 educational macro.

Provides:
    - Global hotkey registration (start / pause / stop).
    - Lightweight main loop that orchestrates the bot and farm manager.
    - Graceful shutdown on Ctrl+C.

This script is intended for educational purposes only.
"""

import logging
import sys
import threading
import time

import keyboard

from bot import Bot
from config import Config
from farm_manager import FarmManager
from screen_scanner import ScreenScanner
from utils import check_privileges, setup_logging


class MacroController:
    """High-level controller binding user hotkeys to bot logic."""

    def __init__(self) -> None:
        setup_logging()
        self.logger = logging.getLogger("MacroController")
        self.config = Config()
        self.scanner = ScreenScanner(self.config)
        self.bot = Bot(self.config, self.scanner)
        self.farm_manager = FarmManager(self.config, self.scanner)
        self._running = threading.Event()
        self._paused = threading.Event()
        self._paused.set()  # not paused by default
        self._stop_flag = False

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def start(self) -> None:
        """Register hotkeys and enter the main loop."""
        check_privileges()
        self.logger.info("Anime Vanguards Auto Farm World 2 - educational macro")
        self.logger.info("Hotkeys:")
        self.logger.info("  Start/Pause: %s", self.config.start_hotkey)
        self.logger.info("  Stop       : %s", self.config.stop_hotkey)

        keyboard.add_hotkey(self.config.start_hotkey, self._toggle_pause)
        keyboard.add_hotkey(self.config.stop_hotkey, self._request_stop)

        try:
            self._main_loop()
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user.")
        finally:
            self._cleanup()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _toggle_pause(self) -> None:
        if self._paused.is_set():
            self._paused.clear()
            self._running.set()
            self.logger.info("Macro started.")
        else:
            self._paused.set()
            self._running.clear()
            self.logger.info("Macro paused.")

    def _request_stop(self) -> None:
        self.logger.info("Stop requested.")
        self._stop_flag = True
        self._running.clear()
        self._paused.set()

    def _main_loop(self) -> None:
        self._running.set()
        while not self._stop_flag:
            self._running.wait()  # block while paused
            if self._stop_flag:
                break
            try:
                self.bot.tick()
                self.farm_manager.tick()
            except Exception as exc:  # pragma: no cover - educational
                self.logger.exception("Loop error: %s", exc)
            time.sleep(self.config.loop_delay)

    def _cleanup(self) -> None:
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        self.logger.info("Macro stopped cleanly.")


def main() -> int:
    """Script entry point."""
    controller = MacroController()
    controller.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
