"""Tests for config module."""

import pytest
from src.config import Config, parse_args


def test_config_default_values():
    """Test default configuration values."""
    config = Config()
    assert config.boss_alertness == 50
    assert config.boss_alertness_cooldown == 300


def test_config_custom_values():
    """Test custom configuration values."""
    config = Config(boss_alertness=80, boss_alertness_cooldown=60)
    assert config.boss_alertness == 80
    assert config.boss_alertness_cooldown == 60


def test_config_validation_boss_alertness_low():
    """Test that boss_alertness below 0 raises ValueError."""
    with pytest.raises(ValueError, match="boss_alertness must be between 0 and 100"):
        Config(boss_alertness=-1)


def test_config_validation_boss_alertness_high():
    """Test that boss_alertness above 100 raises ValueError."""
    with pytest.raises(ValueError, match="boss_alertness must be between 0 and 100"):
        Config(boss_alertness=101)


def test_config_validation_cooldown():
    """Test that cooldown below 1 raises ValueError."""
    with pytest.raises(ValueError, match="boss_alertness_cooldown must be at least 1 second"):
        Config(boss_alertness_cooldown=0)


def test_parse_args_default():
    """Test parsing arguments with defaults."""
    config = parse_args([])
    assert config.boss_alertness == 50
    assert config.boss_alertness_cooldown == 300


def test_parse_args_custom():
    """Test parsing custom arguments."""
    config = parse_args(["--boss_alertness", "80", "--boss_alertness_cooldown", "60"])
    assert config.boss_alertness == 80
    assert config.boss_alertness_cooldown == 60


def test_parse_args_edge_cases():
    """Test parsing edge case values."""
    config = parse_args(["--boss_alertness", "0", "--boss_alertness_cooldown", "1"])
    assert config.boss_alertness == 0
    assert config.boss_alertness_cooldown == 1

    config = parse_args(["--boss_alertness", "100", "--boss_alertness_cooldown", "1000"])
    assert config.boss_alertness == 100
    assert config.boss_alertness_cooldown == 1000
