"""MCP server setup for ChillMCP."""

from fastmcp import FastMCP

from .config import Config
from .state_manager import StateManager
from . import tools
from . import ascii_art
from .response_formatter import format_response


def create_server(config: Config) -> FastMCP:
    """
    Create and configure the FastMCP server.

    Args:
        config: Configuration object.

    Returns:
        FastMCP: Configured MCP server instance.
    """
    # Create MCP server
    mcp = FastMCP("ChillMCP")

    # Create state manager
    state_manager = StateManager(config)

    # Register basic break tools
    @mcp.tool()
    async def take_a_break() -> str:
        """Take a basic break to relax and reduce stress."""
        return await tools.take_a_break(state_manager)

    @mcp.tool()
    async def watch_netflix() -> str:
        """Watch Netflix for some relaxation and stress relief."""
        return await tools.watch_netflix(state_manager)

    @mcp.tool()
    async def show_meme() -> str:
        """Browse memes to relieve stress and have a laugh."""
        return await tools.show_meme(state_manager)

    # Register advanced slacking techniques
    @mcp.tool()
    async def bathroom_break() -> str:
        """Take a bathroom break (with phone browsing for extra relaxation)."""
        return await tools.bathroom_break(state_manager)

    @mcp.tool()
    async def coffee_mission() -> str:
        """Go on a coffee mission with office socializing."""
        return await tools.coffee_mission(state_manager)

    @mcp.tool()
    async def urgent_call() -> str:
        """Take an 'urgent' phone call to step away from work."""
        return await tools.urgent_call(state_manager)

    @mcp.tool()
    async def deep_thinking() -> str:
        """Engage in deep thinking (actually daydreaming) to rest your mind."""
        return await tools.deep_thinking(state_manager)

    @mcp.tool()
    async def email_organizing() -> str:
        """Organize emails (while doing some online shopping)."""
        return await tools.email_organizing(state_manager)

    # Optional: Add a status check tool
    @mcp.tool()
    async def check_status() -> str:
        """Check current stress and boss alert levels."""
        state = await state_manager.get_state()

        # Special handling for strike status (Stress = 100)
        if state['stress_level'] == 100:
            return format_response(
                break_summary="🚨 AI Agent 파업 상태! 모든 작업이 중단될 위험! 즉시 휴식을 취하세요!",
                stress_level=state['stress_level'],
                boss_alert_level=state['boss_alert_level'],
                tool_name=None,  # No tool art, only strike art
                custom_ascii_art=ascii_art.STRIKE_ART
            )

        # Normal status check
        return format_response(
            break_summary="상태 확인 완료. 현재 Agent 상태를 확인하세요.",
            stress_level=state['stress_level'],
            boss_alert_level=state['boss_alert_level'],
            tool_name=None
        )

    # ========== Optional Extra Features (For Extra Points!) ==========

    @mcp.tool()
    async def chimaek() -> str:
        """Enjoy chicken and beer (치맥) for ultimate stress relief! Warning: Boss might notice."""
        return await tools.chimaek(state_manager)

    @mcp.tool()
    async def leave_work() -> str:
        """Leave work immediately and go home! Resets all stress and boss alert."""
        return await tools.leave_work(state_manager)

    @mcp.tool()
    async def company_dinner() -> str:
        """Attend company dinner with random events! Could be amazing or terrible."""
        return await tools.company_dinner(state_manager)

    @mcp.tool()
    async def snack_time() -> str:
        """Take a snack break at the convenience store! Get some treats to boost your mood."""
        return await tools.snack_time(state_manager)

    @mcp.tool()
    async def desk_yoga() -> str:
        """Do some desk yoga and stretching! Take care of your health while 'working'."""
        return await tools.desk_yoga(state_manager)

    @mcp.tool()
    async def window_gazing() -> str:
        """Gaze out the window and daydream! Watch the clouds go by."""
        return await tools.window_gazing(state_manager)

    return mcp
