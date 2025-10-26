"""Statistics and reporting module for ChillMCP server."""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

# History file path (in project root)
HISTORY_FILE = Path(__file__).parent.parent / ".chillmcp_history.json"

def get_break_statistics() -> dict:
    """
    Analyze break history and generate statistics.

    Returns:
        dict: A dictionary containing break statistics.
    """
    if not HISTORY_FILE.exists():
        return {"error": "No break history found."}

    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    if not history:
        return {"error": "Break history is empty."}

    total_breaks = len(history)
    tool_counter = Counter(item['tool_name'] for item in history)
    most_common_tool = tool_counter.most_common(1)[0][0] if tool_counter else "N/A"

    # Analyze break times by hour
    hour_counter = Counter(datetime.fromtimestamp(item['timestamp']).hour for item in history)
    most_common_hour = hour_counter.most_common(1)[0][0] if hour_counter else "N/A"

    return {
        "total_breaks": total_breaks,
        "most_common_tool": most_common_tool,
        "most_common_hour": f"{most_common_hour}:00 - {most_common_hour+1}:00",
        "breaks_by_tool": dict(tool_counter),
    }
