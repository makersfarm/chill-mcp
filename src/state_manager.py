"""State management module for ChillMCP server."""

import asyncio
import json
import os
import random
import time
from pathlib import Path
from typing import Optional

from .config import Config


class StateManager:
    """Manages stress level and boss alert level for the AI agent."""

    # State file path (in project root)
    STATE_FILE = Path(__file__).parent.parent / ".chillmcp_state.json"

    def __init__(self, config: Config):
        """
        Initialize the state manager.

        Args:
            config: Configuration object with boss alertness settings.
        """
        self.config = config
        # Use double underscore for true private variables
        self.__stress_level: int = 0  # 0-100
        self.__boss_alert_level: int = 0  # 0-5
        self._last_stress_update: float = time.time()
        self._last_boss_cooldown: float = time.time()
        self._lock = asyncio.Lock()
        self._loading: bool = False  # Flag to prevent saving during load

        # Load saved state if exists
        self._load_state()

        # Save initial state to ensure file always exists
        self._save_state()

    @property
    def stress_level(self) -> int:
        """Get current stress level (0-100)."""
        return self.__stress_level

    @property
    def _stress_level(self) -> int:
        """Internal property for stress level (getter)."""
        return self.__stress_level

    @_stress_level.setter
    def _stress_level(self, value: int) -> None:
        """
        Internal property for stress level (setter).
        Automatically saves state when value changes.
        """
        # Clamp value to valid range
        value = max(0, min(100, value))

        # Only save if value actually changed and not during loading
        if self.__stress_level != value and not self._loading:
            self.__stress_level = value
            self._save_state()
        else:
            self.__stress_level = value

    @property
    def boss_alert_level(self) -> int:
        """Get current boss alert level (0-5)."""
        return self.__boss_alert_level

    @property
    def _boss_alert_level(self) -> int:
        """Internal property for boss alert level (getter)."""
        return self.__boss_alert_level

    @_boss_alert_level.setter
    def _boss_alert_level(self, value: int) -> None:
        """
        Internal property for boss alert level (setter).
        Automatically saves state when value changes.
        """
        # Clamp value to valid range
        value = max(0, min(5, value))

        # Only save if value actually changed and not during loading
        if self.__boss_alert_level != value and not self._loading:
            self.__boss_alert_level = value
            self._save_state()
        else:
            self.__boss_alert_level = value

    async def update_stress_level(self) -> None:
        """
        Update stress level based on time elapsed.
        Stress increases by at least 1 point per minute if no breaks are taken.
        """
        async with self._lock:
            current_time = time.time()
            elapsed_minutes = (current_time - self._last_stress_update) / 60.0

            if elapsed_minutes >= 1.0:
                # Increase stress by at least 1 point per minute
                stress_increase = int(elapsed_minutes)
                # Setter automatically saves state
                self._stress_level = self._stress_level + stress_increase
                self._last_stress_update = current_time

    async def decrease_stress(self, amount: Optional[int] = None) -> int:
        """
        Decrease stress level by a random or specified amount.

        Args:
            amount: Optional specific amount to decrease. If None, uses random 1-100.

        Returns:
            int: Amount of stress decreased.
        """
        async with self._lock:
            if amount is None:
                amount = random.randint(1, 100)
            else:
                amount = max(1, min(100, amount))

            # Setter automatically saves state
            self._stress_level = self._stress_level - amount
            return amount

    async def increase_stress(self, amount: int) -> int:
        """
        Increase stress level by a specified amount.

        Args:
            amount: Amount to increase stress by (1-100).

        Returns:
            int: Actual amount of stress increased.
        """
        async with self._lock:
            amount = max(1, min(100, amount))
            old_level = self._stress_level
            self._stress_level += amount
            return self._stress_level - old_level

    async def increase_boss_alert(self) -> tuple[bool, int]:
        """
        Potentially increase boss alert level based on boss_alertness probability.

        Returns:
            tuple[bool, int]: (True if boss alert was increased, old boss alert level)
        """
        async with self._lock:
            old_level = self._boss_alert_level
            # Roll the dice based on boss_alertness probability
            if random.randint(1, 100) <= self.config.boss_alertness:
                if self._boss_alert_level < 5:
                    # Setter automatically saves state
                    self._boss_alert_level += 1
                    return (True, old_level)
        return (False, old_level)

    async def change_boss_alert(self, change: int) -> int:
        """
        Change boss alert level by a specified amount (positive or negative).

        Args:
            change: Amount to change boss alert by (can be negative).

        Returns:
            int: New boss alert level.
        """
        async with self._lock:
            self._boss_alert_level = max(0, min(5, self._boss_alert_level + change))
            return self._boss_alert_level

    async def update_boss_cooldown(self) -> None:
        """
        Decrease boss alert level based on cooldown period.
        Boss alert decreases by 1 every boss_alertness_cooldown seconds.
        """
        async with self._lock:
            current_time = time.time()
            elapsed_seconds = current_time - self._last_boss_cooldown

            if elapsed_seconds >= self.config.boss_alertness_cooldown:
                # Calculate how many cooldown periods have passed
                cooldown_periods = int(elapsed_seconds / self.config.boss_alertness_cooldown)
                if self._boss_alert_level > 0:
                    # Setter automatically saves state
                    self._boss_alert_level = self._boss_alert_level - cooldown_periods
                self._last_boss_cooldown = current_time

    async def check_boss_delay(self) -> float:
        """
        Check if boss alert level requires a delay.

        Returns:
            float: Delay in seconds (20 if boss alert is 5, otherwise 0).
        """
        await self.update_boss_cooldown()
        if self._boss_alert_level >= 5:
            return 20.0
        return 0.0

    async def get_state(self) -> dict:
        """
        Get current state as a dictionary.

        Returns:
            dict: Current state with stress_level and boss_alert_level.
        """
        await self.update_stress_level()
        await self.update_boss_cooldown()

        return {
            "stress_level": self._stress_level,
            "boss_alert_level": self._boss_alert_level
        }

    async def reset(self) -> None:
        """Reset state to initial values."""
        async with self._lock:
            # Setter automatically saves state
            self._stress_level = 0
            self._boss_alert_level = 0
            self._last_stress_update = time.time()
            self._last_boss_cooldown = time.time()

    def _save_state(self) -> None:
        """Save current state to file (synchronous)."""
        try:
            state_data = {
                "stress_level": self._stress_level,
                "boss_alert_level": self._boss_alert_level
            }
            with open(self.STATE_FILE, 'w') as f:
                json.dump(state_data, f, indent=2)
        except Exception as e:
            # Fail silently - state persistence is not critical
            pass

    def _load_state(self) -> None:
        """Load state from file if exists (synchronous)."""
        try:
            if self.STATE_FILE.exists():
                # Set loading flag to prevent auto-save during load
                self._loading = True

                with open(self.STATE_FILE, 'r') as f:
                    state_data = json.load(f)

                # Restore stress and boss alert levels
                # Setter is called but won't save because _loading is True
                self._stress_level = state_data.get("stress_level", 0)
                self._boss_alert_level = state_data.get("boss_alert_level", 0)

                # Reset timestamps to current time (don't accumulate time while server was off)
                self._last_stress_update = time.time()
                self._last_boss_cooldown = time.time()

                # Done loading
                self._loading = False
        except Exception as e:
            # Fail silently - if file doesn't exist or is corrupted, start fresh
            self._loading = False
            pass
