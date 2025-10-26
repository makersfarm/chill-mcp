"""
Tests for config module.

This module tests the configuration system for ChillMCP,
including default values, custom values, validation, and argument parsing.
"""

import pytest
from src.config import Config, parse_args


def test_config_default_values():
    """
    Test default configuration values.

    Component: Config initialization
    Purpose: Config 객체가 올바른 기본값으로 초기화되는지 확인

    Initial Conditions:
    - No parameters provided to Config()

    Expected Results:
    - boss_alertness: 50 (50% chance of boss noticing)
    - boss_alertness_cooldown: 300 (5 minutes in seconds)

    Test Status: PASS if both default values are correct
    """
    config = Config()
    assert config.boss_alertness == 50, f"Expected boss_alertness=50, got {config.boss_alertness}"
    assert config.boss_alertness_cooldown == 300, f"Expected cooldown=300, got {config.boss_alertness_cooldown}"


def test_config_custom_values():
    """
    Test custom configuration values.

    Component: Config initialization with parameters
    Purpose: Config 객체가 커스텀 값을 올바르게 설정하는지 확인

    Initial Conditions:
    - boss_alertness=80
    - boss_alertness_cooldown=60

    Expected Results:
    - Values are set exactly as provided
    - No validation errors occur

    Test Status: PASS if custom values are correctly stored
    """
    config = Config(boss_alertness=80, boss_alertness_cooldown=60)
    assert config.boss_alertness == 80, f"Expected boss_alertness=80, got {config.boss_alertness}"
    assert config.boss_alertness_cooldown == 60, f"Expected cooldown=60, got {config.boss_alertness_cooldown}"


def test_config_validation_boss_alertness_low():
    """
    Test boss_alertness lower bound validation.

    Component: Config validation
    Purpose: boss_alertness가 0 미만일 때 ValueError가 발생하는지 확인

    Initial Conditions:
    - boss_alertness=-1 (invalid)

    Expected Results:
    - ValueError is raised
    - Error message: "boss_alertness must be between 0 and 100"

    Test Status: PASS if ValueError is raised with correct message
    """
    with pytest.raises(ValueError, match="boss_alertness must be between 0 and 100"):
        Config(boss_alertness=-1)


def test_config_validation_boss_alertness_high():
    """
    Test boss_alertness upper bound validation.

    Component: Config validation
    Purpose: boss_alertness가 100 초과일 때 ValueError가 발생하는지 확인

    Initial Conditions:
    - boss_alertness=101 (invalid)

    Expected Results:
    - ValueError is raised
    - Error message: "boss_alertness must be between 0 and 100"

    Test Status: PASS if ValueError is raised with correct message
    """
    with pytest.raises(ValueError, match="boss_alertness must be between 0 and 100"):
        Config(boss_alertness=101)


def test_config_validation_cooldown():
    """
    Test cooldown lower bound validation.

    Component: Config validation
    Purpose: boss_alertness_cooldown이 1 미만일 때 ValueError가 발생하는지 확인

    Initial Conditions:
    - boss_alertness_cooldown=0 (invalid)

    Expected Results:
    - ValueError is raised
    - Error message: "boss_alertness_cooldown must be at least 1 second"

    Test Status: PASS if ValueError is raised with correct message
    """
    with pytest.raises(ValueError, match="boss_alertness_cooldown must be at least 1 second"):
        Config(boss_alertness_cooldown=0)


def test_parse_args_default():
    """
    Test command-line argument parsing with defaults.

    Component: parse_args function
    Purpose: 커맨드라인 인자가 없을 때 기본값이 올바르게 설정되는지 확인

    Initial Conditions:
    - Empty argument list []

    Expected Results:
    - boss_alertness: 50 (default)
    - boss_alertness_cooldown: 300 (default)

    Test Status: PASS if default values are correctly applied
    """
    config = parse_args([])
    assert config.boss_alertness == 50, f"Expected default boss_alertness=50, got {config.boss_alertness}"
    assert config.boss_alertness_cooldown == 300, f"Expected default cooldown=300, got {config.boss_alertness_cooldown}"


def test_parse_args_custom():
    """
    Test command-line argument parsing with custom values.

    Component: parse_args function
    Purpose: 커스텀 커맨드라인 인자가 올바르게 파싱되는지 확인

    Initial Conditions:
    - Arguments: ["--boss_alertness", "80", "--boss_alertness_cooldown", "60"]

    Expected Results:
    - boss_alertness: 80
    - boss_alertness_cooldown: 60
    - Values are correctly parsed from command-line arguments

    Test Status: PASS if custom values are correctly parsed
    """
    config = parse_args(["--boss_alertness", "80", "--boss_alertness_cooldown", "60"])
    assert config.boss_alertness == 80, f"Expected boss_alertness=80, got {config.boss_alertness}"
    assert config.boss_alertness_cooldown == 60, f"Expected cooldown=60, got {config.boss_alertness_cooldown}"


def test_parse_args_edge_cases():
    """
    Test command-line argument parsing with edge case values.

    Component: parse_args function
    Purpose: 경계값(최소값, 최대값)이 올바르게 파싱되고 유효성 검사를 통과하는지 확인

    Test Case 1 - Minimum values:
    - boss_alertness: 0 (minimum valid value)
    - boss_alertness_cooldown: 1 (minimum valid value)

    Test Case 2 - Maximum and high values:
    - boss_alertness: 100 (maximum valid value)
    - boss_alertness_cooldown: 1000 (high value, no upper limit)

    Expected Results:
    - All edge case values are accepted
    - No validation errors occur

    Test Status: PASS if all edge cases are correctly handled
    """
    # Test minimum valid values
    config = parse_args(["--boss_alertness", "0", "--boss_alertness_cooldown", "1"])
    assert config.boss_alertness == 0, f"Expected boss_alertness=0, got {config.boss_alertness}"
    assert config.boss_alertness_cooldown == 1, f"Expected cooldown=1, got {config.boss_alertness_cooldown}"

    # Test maximum and high values
    config = parse_args(["--boss_alertness", "100", "--boss_alertness_cooldown", "1000"])
    assert config.boss_alertness == 100, f"Expected boss_alertness=100, got {config.boss_alertness}"
    assert config.boss_alertness_cooldown == 1000, f"Expected cooldown=1000, got {config.boss_alertness_cooldown}"
