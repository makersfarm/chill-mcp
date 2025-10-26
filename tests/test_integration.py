"""Integration tests for ChillMCP server."""

import asyncio
import pytest
import re
import time
from src.config import Config, parse_args
from src.state_manager import StateManager
from src import tools


def validate_response(response_text):
    """
    Validate response format as per README requirements.

    Returns:
        tuple: (is_valid, stress_level, boss_alert_level, error_message)
    """
    # Break Summary
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    break_summary = re.search(break_summary_pattern, response_text, re.MULTILINE)

    # Stress Level
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    stress_match = re.search(stress_level_pattern, response_text)

    # Boss Alert Level
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
    boss_match = re.search(boss_alert_pattern, response_text)

    if not stress_match or not boss_match:
        return False, None, None, "Required fields missing"

    stress_val = int(stress_match.group(1))
    boss_val = int(boss_match.group(1))

    if not (0 <= stress_val <= 100):
        return False, stress_val, boss_val, f"Stress Level out of range: {stress_val}"

    if not (0 <= boss_val <= 5):
        return False, stress_val, boss_val, f"Boss Alert Level out of range: {boss_val}"

    return True, stress_val, boss_val, "Valid response"


@pytest.mark.asyncio
async def test_command_line_arguments():
    """
    Test 1 (REQUIRED): Command-line parameter recognition test.
    Server must recognize --boss_alertness and --boss_alertness_cooldown.
    """
    # Test parsing with custom values
    config = parse_args(["--boss_alertness", "100", "--boss_alertness_cooldown", "10"])

    assert config.boss_alertness == 100, "boss_alertness parameter not recognized"
    assert config.boss_alertness_cooldown == 10, "boss_alertness_cooldown parameter not recognized"

    # Test with different values
    config2 = parse_args(["--boss_alertness", "80", "--boss_alertness_cooldown", "60"])
    assert config2.boss_alertness == 80
    assert config2.boss_alertness_cooldown == 60

    # Test defaults
    config3 = parse_args([])
    assert config3.boss_alertness == 50
    assert config3.boss_alertness_cooldown == 300


@pytest.mark.asyncio
async def test_continuous_break_sequence():
    """
    Test 2 (REQUIRED): Continuous break test.
    Call multiple tools in sequence and verify Boss Alert Level increases.
    """
    config = Config(boss_alertness=100, boss_alertness_cooldown=300)  # 100% alert chance
    state_manager = StateManager(config)
    state_manager._stress_level = 50

    initial_boss_alert = state_manager.boss_alert_level

    # Take multiple breaks
    for _ in range(3):
        response = await tools.take_a_break(state_manager)
        is_valid, stress, boss_alert, msg = validate_response(response)
        assert is_valid, f"Invalid response: {msg}"

    # Boss alert should have increased
    final_boss_alert = state_manager.boss_alert_level
    assert final_boss_alert > initial_boss_alert, "Boss Alert Level should increase with 100% alertness"


@pytest.mark.asyncio
async def test_stress_accumulation():
    """
    Test 3 (REQUIRED): Stress accumulation test.
    Verify stress level increases over time without breaks.
    """
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Set last update to 3 minutes ago
    state_manager._last_stress_update = time.time() - 180

    initial_stress = state_manager.stress_level

    # Update stress
    await state_manager.update_stress_level()

    final_stress = state_manager.stress_level
    assert final_stress >= initial_stress + 3, "Stress should increase by at least 3 points after 3 minutes"


@pytest.mark.asyncio
async def test_delay_at_boss_alert_5():
    """
    Test 4 (REQUIRED): Delay test.
    Verify 20 second delay when Boss Alert Level reaches 5.
    """
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)
    state_manager._boss_alert_level = 5
    state_manager._stress_level = 50

    start_time = time.time()
    response = await tools.take_a_break(state_manager)
    elapsed_time = time.time() - start_time

    is_valid, stress, boss_alert, msg = validate_response(response)
    assert is_valid, f"Invalid response: {msg}"
    assert elapsed_time >= 20.0, f"Expected 20 second delay, got {elapsed_time:.2f} seconds"


@pytest.mark.asyncio
async def test_response_parsing():
    """
    Test 5 (REQUIRED): Response parsing test.
    Verify that responses can be parsed correctly with regex.
    """
    config = Config(boss_alertness=50, boss_alertness_cooldown=300)
    state_manager = StateManager(config)
    state_manager._stress_level = 75

    # Test all tools
    tools_to_test = [
        tools.take_a_break,
        tools.watch_netflix,
        tools.show_meme,
        tools.bathroom_break,
        tools.coffee_mission,
        tools.urgent_call,
        tools.deep_thinking,
        tools.email_organizing,
    ]

    for tool_func in tools_to_test:
        response = await tool_func(state_manager)
        is_valid, stress, boss_alert, msg = validate_response(response)
        assert is_valid, f"{tool_func.__name__} - {msg}"
        assert stress is not None
        assert boss_alert is not None


@pytest.mark.asyncio
async def test_boss_alert_cooldown():
    """
    Test 6 (REQUIRED): Cooldown test.
    Verify Boss Alert Level decreases according to cooldown parameter.
    """
    config = Config(boss_alertness=0, boss_alertness_cooldown=5)  # 5 second cooldown
    state_manager = StateManager(config)
    state_manager._boss_alert_level = 3

    # Set last cooldown to 10 seconds ago (2 cooldown periods)
    state_manager._last_boss_cooldown = time.time() - 10

    await state_manager.update_boss_cooldown()

    # Boss alert should have decreased by 2 (10 seconds / 5 second cooldown)
    assert state_manager.boss_alert_level == 1, f"Expected Boss Alert Level 1, got {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_boss_alertness_probability():
    """
    Test boss alertness probability.
    With 100% alertness, boss alert should always increase.
    With 0% alertness, boss alert should never increase.
    """
    # Test 100% alertness
    config_high = Config(boss_alertness=100, boss_alertness_cooldown=300)
    state_manager_high = StateManager(config_high)

    increased_count = 0
    for _ in range(10):
        boss_increased, old_level = await state_manager_high.increase_boss_alert()
        if boss_increased:
            increased_count += 1
        if state_manager_high.boss_alert_level >= 5:
            break

    assert increased_count >= 5, "With 100% alertness, boss alert should increase consistently"

    # Test 0% alertness
    config_low = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager_low = StateManager(config_low)

    increased_count = 0
    for _ in range(10):
        boss_increased, old_level = await state_manager_low.increase_boss_alert()
        if boss_increased:
            increased_count += 1

    assert increased_count == 0, "With 0% alertness, boss alert should never increase"


@pytest.mark.asyncio
async def test_stress_level_bounds():
    """Test that stress level stays within 0-100 bounds."""
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Test upper bound
    state_manager._stress_level = 95
    state_manager._last_stress_update = time.time() - 600  # 10 minutes ago
    await state_manager.update_stress_level()
    assert state_manager.stress_level <= 100

    # Test lower bound
    state_manager._stress_level = 5
    await state_manager.decrease_stress(100)
    assert state_manager.stress_level >= 0


@pytest.mark.asyncio
async def test_boss_alert_level_bounds():
    """Test that boss alert level stays within 0-5 bounds."""
    config = Config(boss_alertness=100, boss_alertness_cooldown=1)
    state_manager = StateManager(config)

    # Test upper bound
    for _ in range(10):
        await state_manager.increase_boss_alert()
    assert state_manager.boss_alert_level <= 5

    # Test lower bound
    state_manager._boss_alert_level = 2
    state_manager._last_boss_cooldown = time.time() - 100
    await state_manager.update_boss_cooldown()
    assert state_manager.boss_alert_level >= 0


@pytest.mark.asyncio
async def test_full_scenario():
    """
    Full integration test simulating a typical usage scenario.
    """
    config = Config(boss_alertness=50, boss_alertness_cooldown=10)
    state_manager = StateManager(config)

    # Start with some stress
    state_manager._stress_level = 80

    # Take several breaks
    for i in range(5):
        response = await tools.take_a_break(state_manager)
        is_valid, stress, boss_alert, msg = validate_response(response)
        assert is_valid, f"Break {i+1} - {msg}"

        # Verify stress decreased
        assert stress < 80, f"Break {i+1} - Stress should decrease"

    # Get final state
    final_state = await state_manager.get_state()
    assert 0 <= final_state["stress_level"] <= 100
    assert 0 <= final_state["boss_alert_level"] <= 5
