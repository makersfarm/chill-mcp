"""Tests for tools module."""

import pytest
import re
from src.config import Config
from src.state_manager import StateManager
from src import tools


@pytest.fixture
def config():
    """Create a test configuration."""
    return Config(boss_alertness=0, boss_alertness_cooldown=300)  # 0% to avoid randomness


@pytest.fixture
def state_manager(config):
    """Create a state manager instance."""
    return StateManager(config)


def validate_response(response_text):
    """Validate that response has required format."""
    # Check for Break Summary
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    break_summary = re.search(break_summary_pattern, response_text, re.MULTILINE)
    assert break_summary is not None, "Break Summary not found"

    # Check for Stress Level
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    stress_match = re.search(stress_level_pattern, response_text)
    assert stress_match is not None, "Stress Level not found"
    stress_val = int(stress_match.group(1))
    assert 0 <= stress_val <= 100, f"Stress Level out of range: {stress_val}"

    # Check for Boss Alert Level
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
    boss_match = re.search(boss_alert_pattern, response_text)
    assert boss_match is not None, "Boss Alert Level not found"
    boss_val = int(boss_match.group(1))
    assert 0 <= boss_val <= 5, f"Boss Alert Level out of range: {boss_val}"

    return True


@pytest.mark.asyncio
async def test_take_a_break(state_manager):
    """Test take_a_break tool."""
    state_manager._stress_level = 50
    response = await tools.take_a_break(state_manager)

    assert validate_response(response)
    assert state_manager.stress_level < 50  # Stress should decrease


@pytest.mark.asyncio
async def test_watch_netflix(state_manager):
    """Test watch_netflix tool."""
    state_manager._stress_level = 60
    response = await tools.watch_netflix(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_show_meme(state_manager):
    """Test show_meme tool."""
    state_manager._stress_level = 40
    response = await tools.show_meme(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_bathroom_break(state_manager):
    """Test bathroom_break tool."""
    state_manager._stress_level = 70
    response = await tools.bathroom_break(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_coffee_mission(state_manager):
    """Test coffee_mission tool."""
    state_manager._stress_level = 55
    response = await tools.coffee_mission(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_urgent_call(state_manager):
    """Test urgent_call tool."""
    state_manager._stress_level = 80
    response = await tools.urgent_call(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_deep_thinking(state_manager):
    """Test deep_thinking tool."""
    state_manager._stress_level = 45
    response = await tools.deep_thinking(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_email_organizing(state_manager):
    """Test email_organizing tool."""
    state_manager._stress_level = 65
    response = await tools.email_organizing(state_manager)

    assert validate_response(response)


@pytest.mark.asyncio
async def test_boss_alert_delay(state_manager):
    """Test that tools respect boss alert level 5 delay."""
    import time

    state_manager._boss_alert_level = 5
    state_manager._stress_level = 50

    start_time = time.time()
    response = await tools.take_a_break(state_manager)
    elapsed_time = time.time() - start_time

    assert validate_response(response)
    assert elapsed_time >= 20.0  # Should have 20 second delay
