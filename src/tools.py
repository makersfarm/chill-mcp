"""Break tools for the ChillMCP server."""

import asyncio
import random
from typing import List

from .response_formatter import format_response
from .state_manager import StateManager


# Fun messages for each break type
TAKE_A_BREAK_MESSAGES = [
    "🛋️ Stretching and relaxing for a moment...",
    "☕ Taking a well-deserved breather!",
    "🌬️ Deep breath in... and out. Ahhh, refreshing!",
    "💆 Quick relaxation session complete!",
]

NETFLIX_MESSAGES = [
    "📺 Binge-watching the latest series... just one more episode!",
    "🍿 Netflix and chill mode activated!",
    "🎬 Catching up on that trending show everyone's talking about!",
    "📺 'Just 5 minutes'... 2 hours later...",
]

MEME_MESSAGES = [
    "😂 LMAO! This meme is pure gold!",
    "🤣 Scrolling through dank memes... can't stop laughing!",
    "😆 Found the perfect meme to share with the team!",
    "😹 These cat memes never get old!",
]

BATHROOM_MESSAGES = [
    "🛁 Bathroom break! Actually just browsing social media... 📱",
    "🚽 'Nature calls'... *opens Instagram*",
    "🧻 Extended bathroom session with quality phone time!",
    "🚪 Bathroom escape successful! Phone battery at 20% though...",
]

COFFEE_MESSAGES = [
    "☕ Coffee run! Taking the scenic route through all departments...",
    "☕ Making coffee... visiting every colleague on the way!",
    "☕ Coffee mission: 50% coffee, 50% office gossip!",
    "☕ Premium blend brewing... and chatting about last night's game!",
]

URGENT_CALL_MESSAGES = [
    "📞 'Sorry, urgent call!' *walks out to check phone*",
    "📱 'One sec, important call!' *actually checking memes*",
    "☎️ Emergency call excuse activated! Fresh air time!",
    "📞 'Family emergency!' *scrolling through social media outside*",
]

DEEP_THINKING_MESSAGES = [
    "🤔 Deep in thought... definitely not daydreaming about vacation!",
    "💭 Contemplating solutions... actually thinking about lunch!",
    "🧠 Strategic planning mode... planning weekend activities!",
    "💡 Innovation thinking time... pondering what's for dinner!",
]

EMAIL_ORGANIZING_MESSAGES = [
    "📧 Organizing inbox... browsing online shopping deals!",
    "📨 Email cleanup in progress... checking out sneaker drops!",
    "📬 Important email sorting... window shopping for gadgets!",
    "📮 Inbox zero attempt... cart full of random stuff!",
]


async def execute_break_tool(
    state_manager: StateManager,
    messages: List[str],
    tool_name: str
) -> str:
    """
    Execute a break tool with common logic.

    Args:
        state_manager: The state manager instance.
        tool_name: Name of the tool being executed.
        messages: List of possible messages for this break type.

    Returns:
        str: Formatted response.
    """
    # Check if boss is watching (alert level 5 = 20 second delay)
    delay = await state_manager.check_boss_delay()
    if delay > 0:
        await asyncio.sleep(delay)

    # Update stress level (auto-increase based on time)
    await state_manager.update_stress_level()

    # Decrease stress from taking a break
    stress_decrease = await state_manager.decrease_stress()

    # Potentially increase boss alert
    await state_manager.increase_boss_alert()

    # Get current state
    state = await state_manager.get_state()

    # Pick a random message
    message = random.choice(messages)

    return format_response(
        break_summary=message,
        stress_level=state["stress_level"],
        boss_alert_level=state["boss_alert_level"]
    )


# Basic break tools
async def take_a_break(state_manager: StateManager) -> str:
    """
    Take a basic break to relax.

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, TAKE_A_BREAK_MESSAGES, "take_a_break")


async def watch_netflix(state_manager: StateManager) -> str:
    """
    Watch Netflix for some relaxation.

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, NETFLIX_MESSAGES, "watch_netflix")


async def show_meme(state_manager: StateManager) -> str:
    """
    Browse memes for stress relief.

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, MEME_MESSAGES, "show_meme")


# Advanced slacking techniques
async def bathroom_break(state_manager: StateManager) -> str:
    """
    Take a bathroom break (with phone browsing).

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, BATHROOM_MESSAGES, "bathroom_break")


async def coffee_mission(state_manager: StateManager) -> str:
    """
    Go on a coffee mission with office socializing.

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, COFFEE_MESSAGES, "coffee_mission")


async def urgent_call(state_manager: StateManager) -> str:
    """
    Take an 'urgent' phone call.

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, URGENT_CALL_MESSAGES, "urgent_call")


async def deep_thinking(state_manager: StateManager) -> str:
    """
    Engage in deep thinking (actually daydreaming).

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, DEEP_THINKING_MESSAGES, "deep_thinking")


async def email_organizing(state_manager: StateManager) -> str:
    """
    Organize emails (while online shopping).

    Args:
        state_manager: The state manager instance.

    Returns:
        str: Formatted response.
    """
    return await execute_break_tool(state_manager, EMAIL_ORGANIZING_MESSAGES, "email_organizing")
