"""Quick test for new optional tools with state verification."""

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
    """Test new optional tools with state verification."""
    print("="*60)
    print("Testing New Optional Tools with Assertions")
    print("="*60)

    # Create config and state manager
    config = Config(boss_alertness=50, boss_alertness_cooldown=300)
    state_manager = StateManager(config)

    # Test chimaek
    print("\n\n🍗🍺 Testing: chimaek")
    print("-"*60)
    try:
        # Set initial state
        await state_manager.increase_stress(50)
        initial_state = await state_manager.get_state()
        print(f"Initial state: stress={initial_state['stress_level']}, boss={initial_state['boss_alert_level']}")

        result = await tools.chimaek(state_manager)
        print(result)

        final_state = await state_manager.get_state()
        print(f"Final state: stress={final_state['stress_level']}, boss={final_state['boss_alert_level']}")

        # Verify state changes
        assert final_state['stress_level'] < initial_state['stress_level'], "Chimaek should decrease stress"
        assert final_state['boss_alert_level'] > initial_state['boss_alert_level'], "Chimaek should increase boss alert"
        print("\n✅ Chimaek works correctly!")
    except AssertionError as e:
        print(f"\n❌ Chimaek assertion failed: {e}")
    except Exception as e:
        print(f"\n❌ Chimaek failed: {e}")

    # Reset state
    await state_manager.reset()

    # Test leave_work
    print("\n\n🏃 Testing: leave_work")
    print("-"*60)
    try:
        # Set some stress and boss alert first
        await state_manager.increase_stress(60)
        await state_manager.change_boss_alert(3)
        initial_state = await state_manager.get_state()
        print(f"Before leave: stress={initial_state['stress_level']}, boss={initial_state['boss_alert_level']}")

        result = await tools.leave_work(state_manager)
        print(result)

        final_state = await state_manager.get_state()
        print(f"After leave: stress={final_state['stress_level']}, boss={final_state['boss_alert_level']}")

        # Verify everything is reset to 0
        assert final_state['stress_level'] == 0, "Leave work should reset stress to 0"
        assert final_state['boss_alert_level'] == 0, "Leave work should reset boss alert to 0"
        print("\n✅ Leave work works correctly!")
    except AssertionError as e:
        print(f"\n❌ Leave work assertion failed: {e}")
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
            initial_state = await state_manager.get_state()

            result = await tools.company_dinner(state_manager)
            print(result)

            final_state = await state_manager.get_state()

            # Verify state changed (either stress or boss alert should have changed)
            state_changed = (
                final_state['stress_level'] != initial_state['stress_level'] or
                final_state['boss_alert_level'] != initial_state['boss_alert_level']
            )
            assert state_changed, "Company dinner should change state"
            print("\n✅ Company dinner works correctly!")
            await state_manager.reset()
        except AssertionError as e:
            print(f"\n❌ Company dinner assertion failed: {e}")
            break
        except Exception as e:
            print(f"\n❌ Company dinner failed: {e}")
            break

    print("\n\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_new_tools())
