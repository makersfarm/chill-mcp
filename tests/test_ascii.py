"""Manual test script to see ASCII art in action."""

import asyncio
import sys
import os

# Windows UTF-8 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.config import Config
from src.state_manager import StateManager
from src import tools


async def test_ascii_art():
    """Test all tools with ASCII art."""
    print("="*60)
    print("ChillMCP ASCII Art Test")
    print("="*60)

    # Create config and state manager
    config = Config(boss_alertness=50, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Test basic tools
    print("\n\n🛋️  Testing: take_a_break")
    print("-"*60)
    result = await tools.take_a_break(state_manager)
    print(result)

    print("\n\n📺 Testing: watch_netflix")
    print("-"*60)
    result = await tools.watch_netflix(state_manager)
    print(result)

    print("\n\n😂 Testing: show_meme")
    print("-"*60)
    result = await tools.show_meme(state_manager)
    print(result)

    print("\n\n🚽 Testing: bathroom_break")
    print("-"*60)
    result = await tools.bathroom_break(state_manager)
    print(result)

    print("\n\n☕ Testing: coffee_mission")
    print("-"*60)
    result = await tools.coffee_mission(state_manager)
    print(result)

    print("\n\n📞 Testing: urgent_call")
    print("-"*60)
    result = await tools.urgent_call(state_manager)
    print(result)

    print("\n\n💭 Testing: deep_thinking")
    print("-"*60)
    result = await tools.deep_thinking(state_manager)
    print(result)

    print("\n\n📧 Testing: email_organizing")
    print("-"*60)
    result = await tools.email_organizing(state_manager)
    print(result)

    # Test optional features
    print("\n\n🍗🍺 Testing: chimaek (치맥)")
    print("-"*60)
    result = await tools.chimaek(state_manager)
    print(result)

    print("\n\n🏃 Testing: leave_work (퇴근)")
    print("-"*60)
    result = await tools.leave_work(state_manager)
    print(result)

    print("\n\n🍻 Testing: company_dinner (회식)")
    print("-"*60)
    result = await tools.company_dinner(state_manager)
    print(result)

    print("\n\n" + "="*60)
    print("Test Complete!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_ascii_art())
