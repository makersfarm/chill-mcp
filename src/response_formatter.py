"""Response formatting utilities for ChillMCP server."""


def format_response(break_summary: str, stress_level: int, boss_alert_level: int) -> str:
    """
    Format a standard response for break tools.

    The response format is parseable using regex patterns as specified in the requirements.

    Args:
        break_summary: Description of the break activity (free-form text).
        stress_level: Current stress level (0-100).
        boss_alert_level: Current boss alert level (0-5).

    Returns:
        str: Formatted response text.
    """
    # Ensure values are within valid ranges
    stress_level = max(0, min(100, stress_level))
    boss_alert_level = max(0, min(5, boss_alert_level))

    response = f"{break_summary}\n\n"
    response += f"Break Summary: {break_summary}\n"
    response += f"Stress Level: {stress_level}\n"
    response += f"Boss Alert Level: {boss_alert_level}"

    return response
