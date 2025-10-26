"""
Tests for state_manager module.

This module tests the StateManager class which handles:
- Stress level management (increase/decrease)
- Boss alert level management
- Cooldown mechanisms
- Time-based automatic stress increase
- State retrieval and reset

The StateManager is the core component that tracks the AI agent's
stress and the boss's suspicion level throughout the workday.
"""

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
    """
    Test initial state values.

    Component: StateManager initialization
    Purpose: StateManager가 올바른 초기 상태로 시작하는지 확인

    Initial Conditions:
    - New StateManager instance created

    Expected Results:
    - Stress Level: 0 (completely relaxed at start)
    - Boss Alert Level: 0 (boss is not suspicious yet)

    Test Status: PASS if both initial values are 0
    """
    assert state_manager.stress_level == 0, f"Expected initial stress=0, got {state_manager.stress_level}"
    assert state_manager.boss_alert_level == 0, f"Expected initial boss alert=0, got {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_decrease_stress(state_manager):
    """
    Test stress decrease with specific amount.

    Component: StateManager.decrease_stress()
    Purpose: 지정된 양만큼 스트레스가 정확히 감소하는지 확인

    Initial Conditions:
    - Stress Level: 50

    Test Action:
    - Decrease stress by 30

    Expected Results:
    - Return value: 30 (actual decrease amount)
    - Final stress level: 20 (50 - 30)

    Test Status: PASS if stress decreases by exact amount
    """
    # Set initial stress
    state_manager._stress_level = 50

    # Decrease stress by specific amount
    amount = await state_manager.decrease_stress(30)
    assert amount == 30, f"Expected decrease amount=30, got {amount}"
    assert state_manager.stress_level == 20, f"Expected stress=20, got {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_decrease_stress_random(state_manager):
    """
    Test random stress decrease.

    Component: StateManager.decrease_stress() without amount parameter
    Purpose: amount 파라미터 없이 호출 시 랜덤 감소가 올바르게 작동하는지 확인

    Initial Conditions:
    - Stress Level: 100

    Test Action:
    - Decrease stress by random amount (no parameter)

    Expected Results:
    - Decrease amount is between 1 and 100
    - Final stress level is between 0 and 99
    - Random value is within valid range

    Test Status: PASS if random decrease is within expected bounds
    """
    state_manager._stress_level = 100

    amount = await state_manager.decrease_stress()
    assert 1 <= amount <= 100, f"Random decrease amount {amount} is out of range [1, 100]"
    assert 0 <= state_manager.stress_level <= 99, f"Stress level {state_manager.stress_level} is out of range"


@pytest.mark.asyncio
async def test_decrease_stress_floor(state_manager):
    """
    Test stress floor (cannot go below 0).

    Component: StateManager.decrease_stress() boundary check
    Purpose: 스트레스가 0 아래로 내려가지 않는지 확인 (하한선 검증)

    Initial Conditions:
    - Stress Level: 10

    Test Action:
    - Attempt to decrease stress by 50 (more than current)

    Expected Results:
    - Stress level stops at 0 (does not go negative)
    - No errors occur

    Test Status: PASS if stress level is exactly 0
    """
    state_manager._stress_level = 10

    await state_manager.decrease_stress(50)
    assert state_manager.stress_level == 0, f"Expected stress floor=0, got {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_stress_auto_increase(state_manager):
    """
    Test automatic stress increase over time.

    Component: StateManager.update_stress_level()
    Purpose: 시간이 지남에 따라 스트레스가 자동으로 증가하는지 확인 (분당 1포인트)

    Initial Conditions:
    - Stress Level: 0
    - Last update: 2 minutes ago (simulated)

    Test Action:
    - Call update_stress_level()

    Expected Results:
    - Stress increases by at least 2 points (1 point per minute)
    - Time-based stress accumulation works correctly

    Test Status: PASS if stress increased by at least 2
    """
    # Set last update to 2 minutes ago
    state_manager._last_stress_update = time.time() - 120

    await state_manager.update_stress_level()
    assert state_manager.stress_level >= 2, f"Expected stress >= 2 after 2 minutes, got {state_manager.stress_level}"


@pytest.mark.asyncio
async def test_boss_alert_increase_100_percent(state_manager):
    """
    Test boss alert increases with 100% probability.

    Component: StateManager.increase_boss_alert()
    Purpose: boss_alertness=100일 때 항상 경고가 증가하는지 확인

    Initial Conditions:
    - Boss Alertness: 100% (always notices)
    - Boss Alert Level: 0

    Test Action:
    - Call increase_boss_alert() 5 times

    Expected Results:
    - Boss alert increases all 5 times
    - 100% probability works correctly

    Test Status: PASS if increased_count == 5
    """
    # Set boss alertness to 100%
    state_manager.config.boss_alertness = 100

    # Try multiple times
    increased_count = 0
    for _ in range(5):
        if await state_manager.increase_boss_alert():
            increased_count += 1

    assert increased_count == 5, f"Expected 5 increases with 100% alertness, got {increased_count}"


@pytest.mark.asyncio
async def test_boss_alert_max_level(state_manager):
    """
    Test boss alert level ceiling (cannot exceed 5).

    Component: StateManager.increase_boss_alert() boundary check
    Purpose: Boss Alert Level이 최대값 5를 초과하지 않는지 확인

    Initial Conditions:
    - Boss Alertness: 100%
    - Boss Alert Level: 5 (already at maximum)

    Test Action:
    - Attempt to increase boss alert

    Expected Results:
    - Boss alert level stays at 5
    - Does not exceed maximum

    Test Status: PASS if level remains 5
    """
    state_manager.config.boss_alertness = 100
    state_manager._boss_alert_level = 5

    await state_manager.increase_boss_alert()
    assert state_manager.boss_alert_level == 5, f"Expected boss alert ceiling=5, got {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_boss_alert_cooldown(state_manager):
    """
    Test boss alert cooldown decreases alert level.

    Component: StateManager.update_boss_cooldown()
    Purpose: 시간이 지남에 따라 Boss Alert Level이 감소하는지 확인

    Initial Conditions:
    - Boss Alert Level: 3
    - Cooldown: 5 seconds (from config)
    - Last cooldown: 10 seconds ago (2 cooldown periods)

    Test Action:
    - Call update_boss_cooldown()

    Expected Results:
    - Boss alert decreases by 2 (10 seconds / 5 second cooldown)
    - Final level: 1 (3 - 2)

    Test Status: PASS if level is 1 after cooldown
    """
    state_manager._boss_alert_level = 3
    state_manager._last_boss_cooldown = time.time() - 10  # 10 seconds ago (2 cooldown periods)

    await state_manager.update_boss_cooldown()
    assert state_manager.boss_alert_level == 1, f"Expected boss alert=1 after cooldown, got {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_boss_alert_cooldown_floor(state_manager):
    """
    Test boss alert level floor (cannot go below 0).

    Component: StateManager.update_boss_cooldown() boundary check
    Purpose: Boss Alert Level이 0 아래로 내려가지 않는지 확인

    Initial Conditions:
    - Boss Alert Level: 1
    - Cooldown: 5 seconds
    - Last cooldown: 20 seconds ago (4 cooldown periods)

    Test Action:
    - Call update_boss_cooldown()

    Expected Results:
    - Boss alert decreases to 0 and stops
    - Does not go negative

    Test Status: PASS if level is 0
    """
    state_manager._boss_alert_level = 1
    state_manager._last_boss_cooldown = time.time() - 20  # 20 seconds ago

    await state_manager.update_boss_cooldown()
    assert state_manager.boss_alert_level == 0, f"Expected boss alert floor=0, got {state_manager.boss_alert_level}"


@pytest.mark.asyncio
async def test_check_boss_delay_level_5(state_manager):
    """
    Test 20 second delay when boss alert is 5.

    Component: StateManager.check_boss_delay()
    Purpose: Boss Alert Level이 5일 때 20초 지연이 반환되는지 확인

    Initial Conditions:
    - Boss Alert Level: 5 (maximum)

    Test Action:
    - Call check_boss_delay()

    Expected Results:
    - Returns 20.0 seconds delay
    - This delay forces the agent to wait before taking action

    Test Status: PASS if delay == 20.0
    """
    state_manager._boss_alert_level = 5

    delay = await state_manager.check_boss_delay()
    assert delay == 20.0, f"Expected 20 second delay at level 5, got {delay}"


@pytest.mark.asyncio
async def test_check_boss_delay_level_below_5(state_manager):
    """
    Test no delay when boss alert is below 5.

    Component: StateManager.check_boss_delay()
    Purpose: Boss Alert Level이 5 미만일 때 지연이 없는지 확인

    Initial Conditions:
    - Boss Alert Level: 4

    Test Action:
    - Call check_boss_delay()

    Expected Results:
    - Returns 0.0 seconds (no delay)
    - Agent can take action immediately

    Test Status: PASS if delay == 0.0
    """
    state_manager._boss_alert_level = 4

    delay = await state_manager.check_boss_delay()
    assert delay == 0.0, f"Expected no delay below level 5, got {delay}"


@pytest.mark.asyncio
async def test_get_state(state_manager):
    """
    Test getting current state.

    Component: StateManager.get_state()
    Purpose: 현재 상태를 올바르게 반환하는지 확인

    Initial Conditions:
    - Stress Level: 42
    - Boss Alert Level: 3

    Test Action:
    - Call get_state()

    Expected Results:
    - Returns dictionary with current state
    - Contains "stress_level" and "boss_alert_level" keys
    - Stress may increase slightly due to auto-update

    Test Status: PASS if state dictionary is valid
    """
    state_manager._stress_level = 42
    state_manager._boss_alert_level = 3

    state = await state_manager.get_state()
    assert state["stress_level"] >= 42, f"Stress should be >= 42, got {state['stress_level']}"
    assert "boss_alert_level" in state, "State should contain boss_alert_level"
    assert state["boss_alert_level"] == 3, f"Expected boss alert=3, got {state['boss_alert_level']}"


@pytest.mark.asyncio
async def test_reset(state_manager):
    """
    Test resetting state.

    Component: StateManager.reset()
    Purpose: 상태를 초기값으로 리셋하는지 확인

    Initial Conditions:
    - Stress Level: 50
    - Boss Alert Level: 3

    Test Action:
    - Call reset()

    Expected Results:
    - Stress Level: 0
    - Boss Alert Level: 0
    - All state returns to initial values

    Test Status: PASS if both values are 0 after reset
    """
    state_manager._stress_level = 50
    state_manager._boss_alert_level = 3

    await state_manager.reset()
    assert state_manager.stress_level == 0, f"Expected stress=0 after reset, got {state_manager.stress_level}"
    assert state_manager.boss_alert_level == 0, f"Expected boss alert=0 after reset, got {state_manager.boss_alert_level}"
