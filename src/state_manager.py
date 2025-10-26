"""State management module for ChillMCP server."""

import asyncio
import random
import time
from typing import Optional

from .config import Config


class StateManager:
    """Manages stress level and boss alert level for the AI agent."""

    def __init__(self, config: Config):
        """
        Initialize the state manager.

        Args:
            config: Configuration object with boss alertness settings.
        """
        self.config = config
        self._stress_level: int = 0  # 0-100
        self._boss_alert_level: int = 0  # 0-5
        self._last_stress_update: float = time.time()
        self._last_boss_cooldown: float = time.time()
        self._lock = asyncio.Lock()

    @property
    def stress_level(self) -> int:
        """Get current stress level (0-100)."""
        return self._stress_level

    @property
    def boss_alert_level(self) -> int:
        """Get current boss alert level (0-5)."""
        return self._boss_alert_level

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
                self._stress_level = min(100, self._stress_level + stress_increase)
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

            self._stress_level = max(0, self._stress_level - amount)
            return amount

    async def increase_stress(self, amount: int) -> int:
        """
        Increase stress level by a specified amount.

        Args:
            amount: Amount to increase stress by (1-100).

        Returns:
            int: Amount of stress increased.
        """
        async with self._lock:
            amount = max(1, min(100, amount))
            self._stress_level = min(100, self._stress_level + amount)
            return amount

    async def increase_boss_alert(self) -> bool:
        """
        Potentially increase boss alert level based on boss_alertness probability.

        Returns:
            bool: True if boss alert was increased, False otherwise.
        """
        async with self._lock:
            # Roll the dice based on boss_alertness probability
            if random.randint(1, 100) <= self.config.boss_alertness:
                if self._boss_alert_level < 5:
                    self._boss_alert_level += 1
                    return True
        return False

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
                    self._boss_alert_level = max(0, self._boss_alert_level - cooldown_periods)
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
            self._stress_level = 0
            self._boss_alert_level = 0
            self._last_stress_update = time.time()
            self._last_boss_cooldown = time.time()
