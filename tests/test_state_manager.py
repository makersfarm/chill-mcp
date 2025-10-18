"""Tests for state_manager module."""

import asyncio
import pytest
import time
from src.config import Config
from src.state_manager import StateManager


@pytest.fixture
def config():
    """Create a test configuration."""
    return Config(boss_alertness=50, boss_alertness_cooldown=5)


@pytest.fixture
def state_manager(config):
    """Create a state manager instance."""
    return StateManager(config)


@pytest.mark.asyncio
async def test_initial_state(state_manager):
    """Test initial state values."""
    assert state_manager.stress_level == 0
    assert state_manager.boss_alert_level == 0


@pytest.mark.asyncio
async def test_decrease_stress(state_manager):
    """Test stress decrease."""
    # Set initial stress
    state_manager._stress_level = 50

    # Decrease stress
    amount = await state_manager.decrease_stress(30)
    assert amount == 30
    assert state_manager.stress_level == 20


@pytest.mark.asyncio
async def test_decrease_stress_random(state_manager):
    """Test random stress decrease."""
    state_manager._stress_level = 100

    amount = await state_manager.decrease_stress()
    assert 1 <= amount <= 100
    assert 0 <= state_manager.stress_level <= 99


@pytest.mark.asyncio
async def test_decrease_stress_floor(state_manager):
    """Test stress cannot go below 0."""
    state_manager._stress_level = 10

    await state_manager.decrease_stress(50)
    assert state_manager.stress_level == 0


@pytest.mark.asyncio
async def test_stress_auto_increase(state_manager):
    """Test automatic stress increase over time."""
    # Set last update to 2 minutes ago
    state_manager._last_stress_update = time.time() - 120

    await state_manager.update_stress_level()
    assert state_manager.stress_level >= 2  # At least 2 points for 2 minutes


@pytest.mark.asyncio
async def test_boss_alert_increase_100_percent(state_manager):
    """Test boss alert increases with 100% probability."""
    # Set boss alertness to 100%
    state_manager.config.boss_alertness = 100

    # Try multiple times
    increased_count = 0
    for _ in range(5):
        if await state_manager.increase_boss_alert():
            increased_count += 1

    assert increased_count == 5  # Should increase every time


@pytest.mark.asyncio
async def test_boss_alert_max_level(state_manager):
    """Test boss alert level cannot exceed 5."""
    state_manager.config.boss_alertness = 100
    state_manager._boss_alert_level = 5

    await state_manager.increase_boss_alert()
    assert state_manager.boss_alert_level == 5  # Should stay at 5


@pytest.mark.asyncio
async def test_boss_alert_cooldown(state_manager):
    """Test boss alert cooldown decreases alert level."""
    state_manager._boss_alert_level = 3
    state_manager._last_boss_cooldown = time.time() - 10  # 10 seconds ago (2 cooldown periods)

    await state_manager.update_boss_cooldown()
    assert state_manager.boss_alert_level == 1  # Should decrease by 2


@pytest.mark.asyncio
async def test_boss_alert_cooldown_floor(state_manager):
    """Test boss alert level cannot go below 0."""
    state_manager._boss_alert_level = 1
    state_manager._last_boss_cooldown = time.time() - 20  # 20 seconds ago

    await state_manager.update_boss_cooldown()
    assert state_manager.boss_alert_level == 0


@pytest.mark.asyncio
async def test_check_boss_delay_level_5(state_manager):
    """Test 20 second delay when boss alert is 5."""
    state_manager._boss_alert_level = 5

    delay = await state_manager.check_boss_delay()
    assert delay == 20.0


@pytest.mark.asyncio
async def test_check_boss_delay_level_below_5(state_manager):
    """Test no delay when boss alert is below 5."""
    state_manager._boss_alert_level = 4

    delay = await state_manager.check_boss_delay()
    assert delay == 0.0


@pytest.mark.asyncio
async def test_get_state(state_manager):
    """Test getting current state."""
    state_manager._stress_level = 42
    state_manager._boss_alert_level = 3

    state = await state_manager.get_state()
    assert state["stress_level"] >= 42  # May increase due to update
    assert "boss_alert_level" in state


@pytest.mark.asyncio
async def test_reset(state_manager):
    """Test resetting state."""
    state_manager._stress_level = 50
    state_manager._boss_alert_level = 3

    await state_manager.reset()
    assert state_manager.stress_level == 0
    assert state_manager.boss_alert_level == 0
