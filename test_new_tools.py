"""Quick test for new optional tools."""

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


async def test_new_tools():
    """Test new optional tools."""
    print("="*60)
    print("Testing New Optional Tools")
    print("="*60)

    # Create config and state manager
    config = Config(boss_alertness=50, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Test chimaek
    print("\n\n🍗🍺 Testing: chimaek")
    print("-"*60)
    try:
        result = await tools.chimaek(state_manager)
        print(result)
        print("\n✅ Chimaek works!")
    except Exception as e:
        print(f"\n❌ Chimaek failed: {e}")

    # Reset state
    await state_manager.reset()

    # Test leave_work
    print("\n\n🏃 Testing: leave_work")
    print("-"*60)
    try:
        result = await tools.leave_work(state_manager)
        print(result)
        print("\n✅ Leave work works!")
    except Exception as e:
        print(f"\n❌ Leave work failed: {e}")

    # Reset state
    await state_manager.reset()

    # Test company_dinner (run a few times to see different events)
    print("\n\n🍻 Testing: company_dinner (3 times)")
    print("-"*60)
    for i in range(3):
        try:
            print(f"\n--- Attempt {i+1} ---")
            result = await tools.company_dinner(state_manager)
            print(result)
            print("\n✅ Company dinner works!")
            await state_manager.reset()
        except Exception as e:
            print(f"\n❌ Company dinner failed: {e}")
            break

    print("\n\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_new_tools())
