# -*- coding: utf-8 -*-
"""
config.py
=========
Central configuration object for the educational Anime Vanguards Auto
Farm World 2 macro. Adjust the values below to match your screen
resolution and gameplay preferences.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Config:
    # ----- Global hotkeys ------------------------------------------------
    start_hotkey: str = "ctrl+f1"
    stop_hotkey: str = "ctrl+q"

    # ----- Timing --------------------------------------------------------
    loop_delay: float = 0.25
    place_delay: float = 0.4
    quest_delay: float = 1.0
    raid_delay: float = 2.5
    summon_delay: float = 1.5
    boss_ability_delay: float = 0.6
    upgrade_click_delay: float = 0.3
    upgrade_confirm_delay: float = 0.8
    upgrade_interval: int = 20  # loops between upgrade passes

    # ----- Capture region (left, top, width, height) ---------------------
    capture_region: Tuple[int, int, int, int] = (0, 0, 1920, 1080)

    # ----- Placement pattern (relative to capture_region) ----------------
    placement_pattern: List[Tuple[int, int]] = field(
        default_factory=lambda: [
            (320, 540), (420, 540), (520, 540),
            (320, 640), (420, 640), (520, 640),
            (320, 740), (420, 740), (520, 740),
        ]
    )

    # ----- UI element coordinates ----------------------------------------
    quest_button: Tuple[int, int] = (1750, 200)
    raid_button: Tuple[int, int] = (1750, 280)
    summon_button: Tuple[int, int] = (1750, 360)
    upgrade_confirm_button: Tuple[int, int] = (960, 800)

    # ----- Template images (paths) ---------------------------------------
    quest_icon: str = "templates/quest_icon.png"
    raid_icon: str = "templates/raid_icon.png"
    boss_icon: str = "templates/boss_icon.png"
    summon_icon: str = "templates/summon_icon.png"
    upgrade_icon: str = "templates/upgrade_icon.png"

    # ----- Resource regions (left, top, width, height) -------------------
    coin_region: Tuple[int, int, int, int] = (40, 10, 120, 32)
    xp_region: Tuple[int, int, int, int] = (180, 10, 120, 32)

    # ----- Item / upgrade slots ------------------------------------------
    item_slots: List[Tuple[int, int]] = field(
        default_factory=lambda: [(60 + i * 60, 950) for i in range(8)]
    )
    upgrade_targets: List[Tuple[int, int]] = field(
        default_factory=lambda: [
            (320, 540), (420, 540), (520, 540),
        ]
    )

    # ----- Visual hints --------------------------------------------------
    occupied_slot_color: Tuple[int, int, int] = (40, 40, 40)

    # ----- Limits --------------------------------------------------------
    summon_limit: int = 10

    # ----- Boss rotation ability positions -------------------------------
    boss_rotation: List[Tuple[int, int]] = field(
        default_factory=lambda: [(1500, 900), (1600, 900), (1700, 900)]
    )
