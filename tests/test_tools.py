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
    """
    Test take_a_break tool.

    Tool: take_a_break
    Purpose: 짧은 휴식을 취하면서 스트레스를 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 50
    - Boss Alert: 0 (config에서 boss_alertness=0 설정)

    Expected Results:
    - Response format is valid (Break Summary, Stress Level, Boss Alert Level)
    - Stress level decreases from initial value (50)
    - Stress level is within valid range (0-100)
    - Boss alert level is within valid range (0-5)

    Test Status: PASS if all assertions succeed
    """
    # Set initial stress level
    state_manager._stress_level = 50
    initial_stress = state_manager.stress_level

    # Execute the tool
    response = await tools.take_a_break(state_manager)

    # Validate response format
    assert validate_response(response), "Response format validation failed"

    # Verify stress decreased
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_watch_netflix(state_manager):
    """
    Test watch_netflix tool.

    Tool: watch_netflix
    Purpose: 넷플릭스 시청으로 스트레스를 크게 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 60
    - Boss Alert: 0

    Expected Results:
    - Response format is valid (Break Summary, Stress Level, Boss Alert Level)
    - Stress level decreases significantly (typically 20-30 points)
    - All values are within valid ranges

    Test Status: PASS if all assertions succeed
    """
    # Set initial stress level
    state_manager._stress_level = 60
    initial_stress = state_manager.stress_level

    # Execute the tool
    response = await tools.watch_netflix(state_manager)

    # Validate response format
    assert validate_response(response), "Response format validation failed"

    # Additional check: stress should have decreased
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_show_meme(state_manager):
    """
    Test show_meme tool.

    Tool: show_meme
    Purpose: 밈을 보여주면서 가벼운 스트레스 해소를 제공하는 도구 테스트

    Initial Conditions:
    - Stress Level: 40
    - Boss Alert: 0

    Expected Results:
    - Response format is valid
    - Stress level decreases moderately (typically 10-20 points)
    - ASCII art meme is displayed in response

    Test Status: PASS if all assertions succeed
    """
    # Set initial stress level
    state_manager._stress_level = 40
    initial_stress = state_manager.stress_level

    # Execute the tool
    response = await tools.show_meme(state_manager)

    # Validate response format
    assert validate_response(response), "Response format validation failed"

    # Verify stress decreased
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_bathroom_break(state_manager):
    """
    Test bathroom_break tool.

    Tool: bathroom_break
    Purpose: 화장실 휴식으로 스트레스를 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 70
    - Boss Alert: 0

    Expected Results:
    - Response format is valid
    - Stress level decreases (typically 5-15 points)
    - Boss alert may increase (depending on boss_alertness setting)

    Test Status: PASS if all assertions succeed
    """
    state_manager._stress_level = 70
    initial_stress = state_manager.stress_level

    response = await tools.bathroom_break(state_manager)

    assert validate_response(response), "Response format validation failed"
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_coffee_mission(state_manager):
    """
    Test coffee_mission tool.

    Tool: coffee_mission
    Purpose: 커피를 마시러 가면서 스트레스를 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 55
    - Boss Alert: 0

    Expected Results:
    - Response format is valid
    - Stress level decreases (typically 10-20 points)
    - Provides energy boost flavor text

    Test Status: PASS if all assertions succeed
    """
    state_manager._stress_level = 55
    initial_stress = state_manager.stress_level

    response = await tools.coffee_mission(state_manager)

    assert validate_response(response), "Response format validation failed"
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_urgent_call(state_manager):
    """
    Test urgent_call tool.

    Tool: urgent_call
    Purpose: 긴급 전화로 자리를 비우면서 스트레스를 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 80
    - Boss Alert: 0

    Expected Results:
    - Response format is valid
    - Stress level decreases significantly (typically 15-25 points)
    - High stress relief due to "urgent" nature

    Test Status: PASS if all assertions succeed
    """
    state_manager._stress_level = 80
    initial_stress = state_manager.stress_level

    response = await tools.urgent_call(state_manager)

    assert validate_response(response), "Response format validation failed"
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_deep_thinking(state_manager):
    """
    Test deep_thinking tool.

    Tool: deep_thinking
    Purpose: 심각한 생각에 잠기는 척하며 스트레스를 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 45
    - Boss Alert: 0

    Expected Results:
    - Response format is valid
    - Stress level decreases (typically 5-15 points)
    - Low suspicion from boss (lower alert probability)

    Test Status: PASS if all assertions succeed
    """
    state_manager._stress_level = 45
    initial_stress = state_manager.stress_level

    response = await tools.deep_thinking(state_manager)

    assert validate_response(response), "Response format validation failed"
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_email_organizing(state_manager):
    """
    Test email_organizing tool.

    Tool: email_organizing
    Purpose: 이메일 정리하는 척하며 스트레스를 감소시키는 도구 테스트

    Initial Conditions:
    - Stress Level: 65
    - Boss Alert: 0

    Expected Results:
    - Response format is valid
    - Stress level decreases moderately (typically 10-20 points)
    - Appears productive, lower boss alert probability

    Test Status: PASS if all assertions succeed
    """
    state_manager._stress_level = 65
    initial_stress = state_manager.stress_level

    response = await tools.email_organizing(state_manager)

    assert validate_response(response), "Response format validation failed"
    assert state_manager.stress_level < initial_stress, f"Stress should decrease: {initial_stress} -> {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_boss_alert_delay(state_manager):
    """
    Test boss alert level 5 delay mechanism.

    Tool: All tools (tested with take_a_break)
    Purpose: Boss Alert Level 5에 도달했을 때 20초 지연 메커니즘 테스트

    Initial Conditions:
    - Stress Level: 50
    - Boss Alert Level: 5 (maximum)

    Expected Results:
    - Response format is valid
    - Tool execution is delayed by exactly 20 seconds
    - Warning message about boss presence is displayed
    - This simulates the boss watching, forcing the agent to wait

    Test Status: PASS if delay >= 20.0 seconds and response is valid
    """
    import time

    # Set boss alert to maximum level
    state_manager._boss_alert_level = 5
    state_manager._stress_level = 50

    # Measure execution time
    start_time = time.time()
    response = await tools.take_a_break(state_manager)
    elapsed_time = time.time() - start_time

    # Validate response format
    assert validate_response(response), "Response format validation failed"

    # Verify 20 second delay was applied
    assert elapsed_time >= 20.0, f"Expected 20 second delay, but got {elapsed_time:.2f} seconds"
