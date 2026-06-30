# -*- coding: utf-8 -*-
"""
farm_manager.py
===============
FarmManager class handling resource acquisition loops for the educational
Anime Vanguards Auto Farm World 2 macro.

Responsibilities:
    - Coin, XP and item farming loops.
    - Automatic unit upgrade when sufficient resources are available.
    - Adaptive delays based on detected game state.
"""

from __future__ import annotations

import logging
import time
from typing import Dict

from config import Config
from screen_scanner import ScreenScanner


class FarmManager:
    """Coordinates long-running resource farming routines."""

    def __init__(self, config: Config, scanner: ScreenScanner) -> None:
        self.config = config
        self.scanner = scanner
        self.logger = logging.getLogger("FarmManager")
        self._stats: Dict[str, int] = {"coins": 0, "xp": 0, "items": 0}
        self._upgrade_cycle = 0

    # ------------------------------------------------------------------ #
    # Main tick
    # ------------------------------------------------------------------ #
    def tick(self) -> None:
        self._farm_coins()
        self._farm_xp()
        self._farm_items()
        if self._upgrade_cycle >= self.config.upgrade_interval:
            self._upgrade_units()
            self._upgrade_cycle = 0
        self._upgrade_cycle += 1

    # ------------------------------------------------------------------ #
    # Resource farming
    # ------------------------------------------------------------------ #
    def _farm_coins(self) -> None:
        try:
            gained = self.scanner.read_coin_delta()
            if gained > 0:
                self._stats["coins"] += gained
                self.logger.debug("Coins: +%d (total %d)", gained, self._stats["coins"])
        except Exception as exc:
            self.logger.warning("Coin farming error: %s", exc)

    def _farm_xp(self) -> None:
        try:
            gained = self.scanner.read_xp_delta()
            if gained > 0:
                self._stats["xp"] += gained
                self.logger.debug("XP: +%d (total %d)", gained, self._stats["xp"])
        except Exception as exc:
            self.logger.warning("XP farming error: %s", exc)

    def _farm_items(self) -> None:
        try:
            slots = self.scanner.find_free_item_slots()
            if slots:
                self._stats["items"] += len(slots)
                self.logger.debug("Items collected: %d", len(slots))
        except Exception as exc:
            self.logger.warning("Item farming error: %s", exc)

    # ------------------------------------------------------------------ #
    # Unit upgrade automation
    # ------------------------------------------------------------------ #
    def _upgrade_units(self) -> None:
        try:
            for unit_pos in self.config.upgrade_targets:
                if self.scanner.is_unit_upgradeable(unit_pos):
                    self.scanner.click(unit_pos)
                    time.sleep(self.config.upgrade_click_delay)
                    self.scanner.click(self.config.upgrade_confirm_button)
                    time.sleep(self.config.upgrade_confirm_delay)
                    self.logger.info("Upgraded unit at %s", unit_pos)
        except Exception as exc:
            self.logger.warning("Upgrade automation error: %s", exc)

    # ------------------------------------------------------------------ #
    # Stats accessors
    # ------------------------------------------------------------------ #
    @property
    def stats(self) -> Dict[str, int]:
        return dict(self._stats)
