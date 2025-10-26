"""
Integration tests for ChillMCP server.

This module contains comprehensive integration tests that verify
the entire ChillMCP system works correctly end-to-end.

Tests are organized by README requirements:
- Test 1 (REQUIRED): Command-line parameter recognition
- Test 2 (REQUIRED): Continuous break sequence
- Test 3 (REQUIRED): Stress accumulation over time
- Test 4 (REQUIRED): Boss Alert Level 5 delay
- Test 5 (REQUIRED): Response parsing
- Test 6 (REQUIRED): Boss alert cooldown

Additional tests verify boundary conditions and full scenarios.
"""

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

    Checks for:
    - Break Summary (text description)
    - Stress Level (0-100)
    - Boss Alert Level (0-5)

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
    ═══════════════════════════════════════════════════════════
    Test 1 (REQUIRED): Command-line parameter recognition test
    ═══════════════════════════════════════════════════════════

    Component: Command-line argument parsing
    Purpose: 서버가 --boss_alertness 및 --boss_alertness_cooldown 파라미터를 인식하는지 확인

    Test Cases:
    1. Custom values (100, 10)
    2. Different custom values (80, 60)
    3. Default values (no arguments)

    Expected Results:
    - All parameter values are correctly recognized and stored
    - Default values are applied when no arguments provided
    - No parsing errors occur

    Test Status: PASS if all three test cases succeed
    """
    # Test Case 1: Custom high values
    config = parse_args(["--boss_alertness", "100", "--boss_alertness_cooldown", "10"])
    assert config.boss_alertness == 100, "boss_alertness parameter not recognized"
    assert config.boss_alertness_cooldown == 10, "boss_alertness_cooldown parameter not recognized"

    # Test Case 2: Different custom values
    config2 = parse_args(["--boss_alertness", "80", "--boss_alertness_cooldown", "60"])
    assert config2.boss_alertness == 80, f"Expected boss_alertness=80, got {config2.boss_alertness}"
    assert config2.boss_alertness_cooldown == 60, f"Expected cooldown=60, got {config2.boss_alertness_cooldown}"

    # Test Case 3: Default values
    config3 = parse_args([])
    assert config3.boss_alertness == 50, f"Expected default boss_alertness=50, got {config3.boss_alertness}"
    assert config3.boss_alertness_cooldown == 300, f"Expected default cooldown=300, got {config3.boss_alertness_cooldown}"


@pytest.mark.asyncio
async def test_continuous_break_sequence():
    """
    ═══════════════════════════════════════════════════════════
    Test 2 (REQUIRED): Continuous break test
    ═══════════════════════════════════════════════════════════

    Component: Boss alert increase mechanism
    Purpose: 연속으로 휴식을 취할 때 Boss Alert Level이 증가하는지 확인

    Initial Conditions:
    - Boss Alertness: 100% (guaranteed increase)
    - Boss Alertness Cooldown: 300 seconds
    - Stress Level: 50
    - Initial Boss Alert: 0

    Test Action:
    - Take 3 consecutive breaks using take_a_break tool
    - Validate each response format

    Expected Results:
    - All responses are valid (correct format)
    - Boss Alert Level increases with each break
    - Final Boss Alert > Initial Boss Alert

    Test Status: PASS if boss alert increases from 0
    """
    # Setup: 100% alertness to guarantee boss notices
    config = Config(boss_alertness=100, boss_alertness_cooldown=300)
    state_manager = StateManager(config)
    state_manager._stress_level = 50

    initial_boss_alert = state_manager.boss_alert_level

    # Take multiple breaks and verify each response
    for i in range(3):
        response = await tools.take_a_break(state_manager)
        is_valid, stress, boss_alert, msg = validate_response(response)
        assert is_valid, f"Break {i+1} - Invalid response: {msg}"

    # Verify boss alert increased
    final_boss_alert = state_manager.boss_alert_level
    assert final_boss_alert > initial_boss_alert, f"Boss Alert should increase: {initial_boss_alert} -> {final_boss_alert}"


@pytest.mark.asyncio
async def test_stress_accumulation():
    """
    ═══════════════════════════════════════════════════════════
    Test 3 (REQUIRED): Stress accumulation test
    ═══════════════════════════════════════════════════════════

    Component: Automatic stress increase over time
    Purpose: 휴식 없이 시간이 지날 때 스트레스가 자동으로 증가하는지 확인

    Initial Conditions:
    - Boss Alertness: 0% (no boss interference)
    - Stress Level: 0
    - Last stress update: 3 minutes ago (simulated)

    Test Action:
    - Call update_stress_level()
    - Simulate 3 minutes of work without breaks

    Expected Results:
    - Stress increases by at least 3 points (1 point per minute)
    - Time-based stress accumulation works correctly
    - Formula: stress += (elapsed_minutes * 1 point/minute)

    Test Status: PASS if stress increased by >= 3
    """
    # Setup: no boss interference
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Simulate 3 minutes of work
    state_manager._last_stress_update = time.time() - 180  # 180 seconds = 3 minutes

    initial_stress = state_manager.stress_level

    # Update stress based on elapsed time
    await state_manager.update_stress_level()

    final_stress = state_manager.stress_level
    assert final_stress >= initial_stress + 3, f"Stress should increase by >= 3 after 3 minutes: {initial_stress} -> {final_stress}"


@pytest.mark.asyncio
async def test_delay_at_boss_alert_5():
    """
    ═══════════════════════════════════════════════════════════
    Test 4 (REQUIRED): Boss Alert Level 5 delay test
    ═══════════════════════════════════════════════════════════

    Component: Boss Alert Level 5 delay mechanism
    Purpose: Boss Alert Level이 5에 도달했을 때 20초 지연이 발생하는지 확인

    Initial Conditions:
    - Boss Alert Level: 5 (maximum, boss is watching!)
    - Stress Level: 50
    - Boss Alertness: 0% (to prevent further increases)

    Test Action:
    - Call take_a_break tool
    - Measure execution time

    Expected Results:
    - Response format is valid
    - Execution time >= 20.0 seconds
    - Agent must wait due to boss watching
    - Warning message about boss presence displayed

    Test Status: PASS if delay >= 20 seconds and response valid
    """
    # Setup: boss alert at maximum
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)
    state_manager._boss_alert_level = 5
    state_manager._stress_level = 50

    # Measure execution time
    start_time = time.time()
    response = await tools.take_a_break(state_manager)
    elapsed_time = time.time() - start_time

    # Validate response
    is_valid, stress, boss_alert, msg = validate_response(response)
    assert is_valid, f"Invalid response: {msg}"

    # Verify 20 second delay
    assert elapsed_time >= 20.0, f"Expected >= 20 second delay at level 5, got {elapsed_time:.2f} seconds"


@pytest.mark.asyncio
async def test_response_parsing():
    """
    ═══════════════════════════════════════════════════════════
    Test 5 (REQUIRED): Response parsing test
    ═══════════════════════════════════════════════════════════

    Component: All tool response formats
    Purpose: 모든 도구의 응답이 올바른 형식으로 파싱되는지 확인

    Tools Tested:
    1. take_a_break - 짧은 휴식
    2. watch_netflix - 넷플릭스 시청
    3. show_meme - 밈 보기
    4. bathroom_break - 화장실 휴식
    5. coffee_mission - 커피 미션
    6. urgent_call - 긴급 전화
    7. deep_thinking - 심각한 생각
    8. email_organizing - 이메일 정리

    Initial Conditions:
    - Boss Alertness: 50%
    - Stress Level: 75 (high stress for testing)

    Expected Results:
    - All 8 tools return valid response format
    - Each response contains:
      * Break Summary (text description)
      * Stress Level (0-100)
      * Boss Alert Level (0-5)
    - Regex parsing works for all tools

    Test Status: PASS if all 8 tools pass validation
    """
    # Setup
    config = Config(boss_alertness=50, boss_alertness_cooldown=300)
    state_manager = StateManager(config)
    state_manager._stress_level = 75

    # List of all tools to test
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

    # Test each tool
    for tool_func in tools_to_test:
        response = await tool_func(state_manager)
        is_valid, stress, boss_alert, msg = validate_response(response)
        assert is_valid, f"{tool_func.__name__} - {msg}"
        assert stress is not None, f"{tool_func.__name__} - stress level not parsed"
        assert boss_alert is not None, f"{tool_func.__name__} - boss alert not parsed"


@pytest.mark.asyncio
async def test_boss_alert_cooldown():
    """
    ═══════════════════════════════════════════════════════════
    Test 6 (REQUIRED): Boss alert cooldown test
    ═══════════════════════════════════════════════════════════

    Component: Boss alert cooldown mechanism
    Purpose: Boss Alert Level이 cooldown 파라미터에 따라 감소하는지 확인

    Initial Conditions:
    - Boss Alertness: 0%
    - Boss Alertness Cooldown: 5 seconds
    - Boss Alert Level: 3
    - Last cooldown: 10 seconds ago (2 cooldown periods)

    Test Action:
    - Call update_boss_cooldown()

    Expected Results:
    - Boss alert decreases by 2 levels (10 sec / 5 sec cooldown = 2 decreases)
    - Final Boss Alert Level: 1 (3 - 2)
    - Formula: decreases = elapsed_time / cooldown_period

    Test Status: PASS if boss alert level is 1
    """
    # Setup: fast cooldown for testing
    config = Config(boss_alertness=0, boss_alertness_cooldown=5)  # 5 second cooldown
    state_manager = StateManager(config)
    state_manager._boss_alert_level = 3

    # Simulate 10 seconds elapsed (2 cooldown periods)
    state_manager._last_boss_cooldown = time.time() - 10

    # Apply cooldown
    await state_manager.update_boss_cooldown()

    # Boss alert should have decreased by 2 (10 seconds / 5 second cooldown)
    assert state_manager.boss_alert_level == 1, f"Expected Boss Alert Level 1 after cooldown, got {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_boss_alertness_probability():
    """
    ═══════════════════════════════════════════════════════════
    Additional Test: Boss alertness probability verification
    ═══════════════════════════════════════════════════════════

    Component: Boss alertness probability system
    Purpose: boss_alertness 확률이 올바르게 작동하는지 확인

    Test Case 1 - 100% Alertness:
    - Boss Alertness: 100%
    - Expected: Boss alert increases every time (10 attempts)
    - Should reach level 5 within 5 attempts

    Test Case 2 - 0% Alertness:
    - Boss Alertness: 0%
    - Expected: Boss alert never increases (10 attempts)
    - Should stay at level 0

    Expected Results:
    - 100% alertness: increased_count >= 5
    - 0% alertness: increased_count == 0
    - Probability system works correctly at extremes

    Test Status: PASS if both cases behave as expected
    """
    # Test Case 1: 100% alertness - boss always notices
    config_high = Config(boss_alertness=100, boss_alertness_cooldown=300)
    state_manager_high = StateManager(config_high)

    increased_count = 0
    for _ in range(10):
        boss_increased, old_level = await state_manager_high.increase_boss_alert()
        if boss_increased:
            increased_count += 1
        if state_manager_high.boss_alert_level >= 5:
            break

    assert increased_count >= 5, f"With 100% alertness, should increase consistently. Got {increased_count} increases"

    # Test Case 2: 0% alertness - boss never notices
    config_low = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager_low = StateManager(config_low)

    increased_count = 0
    for _ in range(10):
        boss_increased, old_level = await state_manager_low.increase_boss_alert()
        if boss_increased:
            increased_count += 1

    assert increased_count == 0, f"With 0% alertness, should never increase. Got {increased_count} increases"


@pytest.mark.asyncio
async def test_stress_level_bounds():
    """
    ═══════════════════════════════════════════════════════════
    Additional Test: Stress level boundary verification
    ═══════════════════════════════════════════════════════════

    Component: Stress level bounds checking
    Purpose: 스트레스 레벨이 0-100 범위를 벗어나지 않는지 확인

    Test Case 1 - Upper Bound (100):
    - Initial Stress: 95
    - Simulate: 10 minutes elapsed (should add 10 points)
    - Expected: Stress stays at or below 100

    Test Case 2 - Lower Bound (0):
    - Initial Stress: 5
    - Action: Decrease by 100 (more than current)
    - Expected: Stress stays at or above 0

    Expected Results:
    - Stress never exceeds 100 (ceiling)
    - Stress never goes below 0 (floor)
    - Boundary checks work correctly

    Test Status: PASS if both bounds are respected
    """
    config = Config(boss_alertness=0, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Test Case 1: Upper bound (ceiling at 100)
    state_manager._stress_level = 95
    state_manager._last_stress_update = time.time() - 600  # 10 minutes ago
    await state_manager.update_stress_level()
    assert state_manager.stress_level <= 100, f"Stress exceeded ceiling: {state_manager.stress_level}"

    # Test Case 2: Lower bound (floor at 0)
    state_manager._stress_level = 5
    await state_manager.decrease_stress(100)
    assert state_manager.stress_level >= 0, f"Stress went below floor: {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_boss_alert_level_bounds():
    """
    ═══════════════════════════════════════════════════════════
    Additional Test: Boss alert level boundary verification
    ═══════════════════════════════════════════════════════════

    Component: Boss alert level bounds checking
    Purpose: Boss Alert Level이 0-5 범위를 벗어나지 않는지 확인

    Test Case 1 - Upper Bound (5):
    - Boss Alertness: 100%
    - Action: Attempt to increase 10 times
    - Expected: Level stops at 5 (does not exceed)

    Test Case 2 - Lower Bound (0):
    - Initial Level: 2
    - Simulate: 100 seconds of cooldown (many periods)
    - Expected: Level stops at 0 (does not go negative)

    Expected Results:
    - Boss alert never exceeds 5 (ceiling)
    - Boss alert never goes below 0 (floor)
    - Boundary checks work correctly

    Test Status: PASS if both bounds are respected
    """
    config = Config(boss_alertness=100, boss_alertness_cooldown=1)
    state_manager = StateManager(config)

    # Test Case 1: Upper bound (ceiling at 5)
    for _ in range(10):
        await state_manager.increase_boss_alert()
    assert state_manager.boss_alert_level <= 5, f"Boss alert exceeded ceiling: {state_manager.boss_alert_level}"

    # Test Case 2: Lower bound (floor at 0)
    state_manager._boss_alert_level = 2
    state_manager._last_boss_cooldown = time.time() - 100
    await state_manager.update_boss_cooldown()
    assert state_manager.boss_alert_level >= 0, f"Boss alert went below floor: {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_full_scenario():
    """
    ═══════════════════════════════════════════════════════════
    Additional Test: Full integration scenario
    ═══════════════════════════════════════════════════════════

    Component: Complete system integration
    Purpose: 실제 사용 시나리오를 시뮬레이션하여 전체 시스템 통합 테스트

    Scenario:
    1. Agent starts with high stress (80)
    2. Takes 5 consecutive breaks to reduce stress
    3. Boss has 50% chance to notice each break
    4. System validates all responses and state changes

    Initial Conditions:
    - Boss Alertness: 50% (realistic probability)
    - Boss Alertness Cooldown: 10 seconds (fast for testing)
    - Stress Level: 80 (high stress)

    Test Actions:
    - Take 5 breaks using take_a_break tool
    - Validate each response format
    - Check stress decreases each time
    - Get final state

    Expected Results:
    - All 5 responses are valid
    - Stress decreases with each break (< initial 80)
    - Final stress is within valid range (0-100)
    - Final boss alert is within valid range (0-5)
    - System handles multiple sequential operations correctly

    Test Status: PASS if all validations succeed
    """
    # Setup: realistic scenario
    config = Config(boss_alertness=50, boss_alertness_cooldown=10)
    state_manager = StateManager(config)

    # Start with high stress (typical stressed agent)
    state_manager._stress_level = 80
    initial_stress = 80

    # Take several breaks to reduce stress
    for i in range(5):
        response = await tools.take_a_break(state_manager)
        is_valid, stress, boss_alert, msg = validate_response(response)
        assert is_valid, f"Break {i+1} - Invalid response: {msg}"

        # Verify stress decreased from initial level
        assert stress < initial_stress, f"Break {i+1} - Stress should decrease from {initial_stress}, got {stress}"

    # Get final state and verify all values are in valid ranges
    final_state = await state_manager.get_state()
    assert 0 <= final_state["stress_level"] <= 100, f"Final stress out of range: {final_state['stress_level']}"
    assert 0 <= final_state["boss_alert_level"] <= 5, f"Final boss alert out of range: {final_state['boss_alert_level']}"
