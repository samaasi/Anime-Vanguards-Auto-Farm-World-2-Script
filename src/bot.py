# -*- coding: utf-8 -*-
"""
bot.py
======
Bot class encapsulating high-level gameplay automation logic for the
educational Anime Vanguards Auto Farm World 2 macro.

Modules covered:
    - Auto placement of units according to configurable patterns.
    - Auto quest progression.
    - Auto raid looping.
    - Auto boss engagement.
    - Auto summon batching.

All methods are intentionally defensive: exceptions are logged and the
bot continues running to maximize stability during long sessions.
"""

from __future__ import annotations

import logging
import time
from typing import List, Tuple

from config import Config
from screen_scanner import ScreenScanner


class Bot:
    """Coordinator for automated gameplay actions."""

    def __init__(self, config: Config, scanner: ScreenScanner) -> None:
        self.config = config
        self.scanner = scanner
        self.logger = logging.getLogger("Bot")
        self._placement_index = 0
        self._raid_counter = 0
        self._summon_count = 0

    # ------------------------------------------------------------------ #
    # Main tick - called by the controller every loop iteration.
    # ------------------------------------------------------------------ #
    def tick(self) -> None:
        """Run one full automation pass."""
        self._auto_place_units()
        self._auto_quest()
        self._auto_raid()
        self._auto_boss()
        self._auto_summon()

    # ------------------------------------------------------------------ #
    # Auto Place
    # ------------------------------------------------------------------ #
    def _auto_place_units(self) -> None:
        pattern: List[Tuple[int, int]] = self.config.placement_pattern
        if self._placement_index >= len(pattern):
            self._placement_index = 0
            return
        target = pattern[self._placement_index]
        try:
            if self.scanner.is_unit_slot_available(target):
                self.scanner.click(target)
                time.sleep(self.config.place_delay)
                self._placement_index += 1
                self.logger.debug("Placed unit at %s", target)
        except Exception as exc:
            self.logger.warning("Auto place failed: %s", exc)

    # ------------------------------------------------------------------ #
    # Auto Quest
    # ------------------------------------------------------------------ #
    def _auto_quest(self) -> None:
        try:
            if self.scanner.quest_available():
                self.scanner.click(self.config.quest_button)
                time.sleep(self.config.quest_delay)
                self.logger.info("Quest accepted.")
        except Exception as exc:
            self.logger.warning("Auto quest failed: %s", exc)

    # ------------------------------------------------------------------ #
    # Auto Raid
    # ------------------------------------------------------------------ #
    def _auto_raid(self) -> None:
        try:
            if self.scanner.raid_ready():
                self.scanner.click(self.config.raid_button)
                self._raid_counter += 1
                self.logger.info("Raid #%d started.", self._raid_counter)
                time.sleep(self.config.raid_delay)
        except Exception as exc:
            self.logger.warning("Auto raid failed: %s", exc)

    # ------------------------------------------------------------------ #
    # Auto Boss
    # ------------------------------------------------------------------ #
    def _auto_boss(self) -> None:
        try:
            boss_pos = self.scanner.find_boss()
            if boss_pos is not None:
                self.logger.info("Boss detected at %s.", boss_pos)
                for ability in self.config.boss_rotation:
                    self.scanner.click(ability)
                    time.sleep(self.config.boss_ability_delay)
        except Exception as exc:
            self.logger.warning("Auto boss failed: %s", exc)

    # ------------------------------------------------------------------ #
    # Auto Summon
    # ------------------------------------------------------------------ #
    def _auto_summon(self) -> None:
        if self._summon_count >= self.config.summon_limit:
            return
        try:
            if self.scanner.summon_available():
                self.scanner.click(self.config.summon_button)
                self._summon_count += 1
                self.logger.info("Summon #%d performed.", self._summon_count)
                time.sleep(self.config.summon_delay)
        except Exception as exc:
            self.logger.warning("Auto summon failed: %s", exc)
