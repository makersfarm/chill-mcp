"""Response formatting utilities for ChillMCP server."""

from . import ascii_art


def format_response(
    break_summary: str,
    stress_level: int,
    boss_alert_level: int,
    tool_name: str = None,
    show_ascii_art: bool = True
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

    response = ""

    # Add ASCII art if enabled and tool name is provided
    if show_ascii_art and tool_name:
        tool_art = ascii_art.get_tool_ascii_art(tool_name)
        if tool_art:
            response += tool_art + "\n"

    # Add status dashboard
    if show_ascii_art:
        dashboard = ascii_art.create_status_dashboard(stress_level, boss_alert_level)
        response += dashboard + "\n"

    # Add boss state if alert level is high
    if show_ascii_art and boss_alert_level >= 3:
        boss_art = ascii_art.get_boss_state_art(boss_alert_level)
        response += boss_art + "\n"

    # Add break summary and required fields
    response += f"{break_summary}\n\n"
    response += f"Break Summary: {break_summary}\n"
    response += f"Stress Level: {stress_level}\n"
    response += f"Boss Alert Level: {boss_alert_level}"

    return response
