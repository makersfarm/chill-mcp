"""Response formatting utilities for ChillMCP server."""

from . import ascii_art


def format_response(
    break_summary: str,
    stress_level: int,
    boss_alert_level: int,
    tool_name: str = None,
    show_ascii_art: bool = True,
    custom_ascii_art: str = None
) -> str:
    """
    Format a standard response for break tools with optional ASCII art.

    The response format is parseable using regex patterns as specified in the requirements.

    Args:
        break_summary: Description of the break activity (free-form text).
        stress_level: Current stress level (0-100).
        boss_alert_level: Current boss alert level (0-5).
        tool_name: Name of the tool being used (for ASCII art lookup).
        show_ascii_art: Whether to include ASCII art in the response.

    Returns:
        str: Formatted response text.
    """
    # Ensure values are within valid ranges
    stress_level = max(0, min(100, stress_level))
    boss_alert_level = max(0, min(5, boss_alert_level))

    # Build ASCII art section if enabled
    ascii_section = ""

    # STRIKE ART takes priority when stress is 100
    if show_ascii_art and stress_level == 100:
        ascii_section = ascii_art.STRIKE_ART + "\n\n"

    # Use custom ASCII art if provided, otherwise use default
    if show_ascii_art and custom_ascii_art:
        ascii_section += custom_ascii_art
    elif show_ascii_art:
        if tool_name:
            tool_art = ascii_art.get_tool_ascii_art(tool_name)
            if tool_art:
                ascii_section += tool_art + "\n"


        if boss_alert_level >= 3:
            boss_art = ascii_art.get_boss_state_art(boss_alert_level)
            ascii_section += boss_art + "\n"

    # Create user-friendly message
    stress_emoji = _get_stress_emoji(stress_level)
    boss_emoji = _get_boss_emoji(boss_alert_level)

    # Special header for strike status
    if stress_level == 100:
        header = "🚨 **긴급! AI Agent 파업 중!** 🚨"
        strike_warning = "\n⚠️ **Stress Level 100 도달! 즉시 휴식이 필요합니다!** ⚠️\n"
    else:
        header = "🎨 **AI Agent 상태 업데이트!**"
        strike_warning = ""

    response = f"""{header}

{break_summary}
{strike_warning}
📊 **현재 상태:**
{stress_emoji} Stress Level: {stress_level}% {_create_progress_bar(stress_level, 100, 10)}
{boss_emoji} Boss Alert: {boss_alert_level}/5 {_create_progress_bar(boss_alert_level, 5, 5)}

"""

    # Add ASCII art instruction for Claude
    if ascii_section:
        response += f"""
🖼️ **ASCII 아트 (사용자에게 코드 블록으로 보여주세요!):**

```
{ascii_section.strip()}
```

"""

    # Add required fields for parsing (at the end)
    response += f"""
---
Break Summary: {break_summary}
Stress Level: {stress_level}
Boss Alert Level: {boss_alert_level}
"""

    return response


def _create_progress_bar(value: int, max_value: int, length: int = 10) -> str:
    """
    Create a text-based progress bar.

    Args:
        value: Current value.
        max_value: Maximum value.
        length: Length of the progress bar.

    Returns:
        str: Progress bar string.
    """
    filled = int((value / max_value) * length)
    empty = length - filled
    return '[' + '█' * filled + '░' * empty + ']'


def _get_stress_emoji(stress_level: int) -> str:
    """Get emoji based on stress level."""
    if stress_level < 20:
        return "😊"
    elif stress_level < 40:
        return "🙂"
    elif stress_level < 60:
        return "😐"
    elif stress_level < 80:
        return "😰"
    else:
        return "😫"


def _get_boss_emoji(boss_alert: int) -> str:
    """Get emoji based on boss alert level."""
    if boss_alert == 0:
        return "😎"
    elif boss_alert == 1:
        return "👀"
    elif boss_alert == 2:
        return "🤨"
    elif boss_alert == 3:
        return "😠"
    elif boss_alert == 4:
        return "💢"
    else:
        return "🚨"
