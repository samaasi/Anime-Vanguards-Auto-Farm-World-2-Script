# -*- coding: utf-8 -*-
"""
screen_scanner.py
=================
Functions and helpers for reading the game screen, detecting UI elements
and locating interactive regions.

Uses OpenCV and PIL for image analysis. All public methods degrade
gracefully on errors and return safe defaults (False / None / 0) so the
macro can continue running.
"""

from __future__ import annotations

import logging
import time
from typing import List, Optional, Tuple

import cv2
import numpy as np
import pyautogui

from config import Config

Point = Tuple[int, int]


class ScreenScanner:
    """Wraps screen capture and template matching primitives."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger = logging.getLogger("ScreenScanner")
        # Safety guard: pyautogui will raise if the cursor strays.
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    # ------------------------------------------------------------------ #
    # Low-level utilities
    # ------------------------------------------------------------------ #
    def grab_screen(self) -> np.ndarray:
        """Capture the configured screen region as a BGR ndarray."""
        region = self.config.capture_region  # (left, top, width, height)
        shot = pyautogui.screenshot(region=region)
        return cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)

    def _match_template(self, template_path: str, threshold: float = 0.8) -> Optional[Point]:
        try:
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                self.logger.warning("Template not found: %s", template_path)
                return None
            screen = self.grab_screen()
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                return max_loc
        except Exception as exc:
            self.logger.warning("Template match failed (%s): %s", template_path, exc)
        return None

    # ------------------------------------------------------------------ #
    # High-level detection API
    # ------------------------------------------------------------------ #
    def is_unit_slot_available(self, position: Point) -> bool:
        """Return True if the slot at *position* appears empty."""
        click_point = self._resolve_position(position)
        try:
            pixel = pyautogui.pixel(*click_point)
            return pixel != self.config.occupied_slot_color
        except Exception as exc:
            self.logger.warning("Slot check failed: %s", exc)
            return False

    def quest_available(self) -> bool:
        return self._match_template(self.config.quest_icon, 0.75) is not None

    def raid_ready(self) -> bool:
        return self._match_template(self.config.raid_icon, 0.75) is not None

    def find_boss(self) -> Optional[Point]:
        return self._match_template(self.config.boss_icon, 0.70)

    def summon_available(self) -> bool:
        return self._match_template(self.config.summon_icon, 0.75) is not None

    # ------------------------------------------------------------------ #
    # Resource readers
    # ------------------------------------------------------------------ #
    def read_coin_delta(self) -> int:
        """Educational stub: read coin delta from a screen region."""
        return self._read_numeric_region(self.config.coin_region)

    def read_xp_delta(self) -> int:
        return self._read_numeric_region(self.config.xp_region)

    def find_free_item_slots(self) -> List[Point]:
        slots: List[Point] = []
        for slot in self.config.item_slots:
            if self.is_unit_slot_available(slot):
                slots.append(slot)
        return slots

    def is_unit_upgradeable(self, unit_pos: Point) -> bool:
        return self._match_template(self.config.upgrade_icon, 0.70) is not None

    # ------------------------------------------------------------------ #
    # Interaction
    # ------------------------------------------------------------------ #
    def click(self, position: Point, button: str = "left") -> None:
        click_point = self._resolve_position(position)
        pyautogui.click(click_point[0], click_point[1], button=button)
        time.sleep(0.02)

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #
    def _resolve_position(self, position: Point) -> Point:
        """Convert a relative config position into absolute screen coords."""
        left, top, _, _ = self.config.capture_region
        return (left + position[0], top + position[1])

    def _read_numeric_region(self, region: Tuple[int, int, int, int]) -> int:
        """Educational placeholder for OCR-based number reading."""
        # In a real implementation pytesseract or a digit template matcher
        # would parse the region. We return 0 to keep the loop safe.
        try:
            pyautogui.screenshot(region=region)
        except Exception:
            return 0
        return 0
