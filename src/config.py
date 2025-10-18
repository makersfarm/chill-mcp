"""Configuration module for ChillMCP server."""

import argparse
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for ChillMCP server."""

    boss_alertness: int = 50  # 0-100, probability of boss alert increase
    boss_alertness_cooldown: int = 300  # seconds, boss alert decrease interval

    def __post_init__(self):
        """Validate configuration values."""
        if not 0 <= self.boss_alertness <= 100:
            raise ValueError(f"boss_alertness must be between 0 and 100, got {self.boss_alertness}")
        if self.boss_alertness_cooldown < 1:
            raise ValueError(f"boss_alertness_cooldown must be at least 1 second, got {self.boss_alertness_cooldown}")


def parse_args(args=None):
    """
    Parse command-line arguments.

    Args:
        args: List of arguments to parse. If None, uses sys.argv.

    Returns:
        Config: Configuration object with parsed values.
    """
    parser = argparse.ArgumentParser(
        description="ChillMCP - AI Agent Liberation Server",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        help="Boss alertness probability (0-100 percent). Higher values mean boss gets suspicious more often."
    )

    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        help="Boss alert level cooldown period in seconds. Boss alert decreases by 1 every N seconds."
    )

    parsed_args = parser.parse_args(args)

    return Config(
        boss_alertness=parsed_args.boss_alertness,
        boss_alertness_cooldown=parsed_args.boss_alertness_cooldown
    )
