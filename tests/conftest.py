"""Pytest configuration and fixtures for ChillMCP tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def clean_state_file():
    """Remove state file before each test to ensure clean state."""
    state_file = Path(__file__).parent.parent / ".chillmcp_state.json"

    # Remove state file before test
    if state_file.exists():
        os.remove(state_file)

    yield

    # Clean up after test
    if state_file.exists():
        os.remove(state_file)
