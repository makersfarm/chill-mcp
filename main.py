"""Main entry point for ChillMCP server."""

import sys
from src.config import parse_args
from src.server import create_server


def main():
    """Run the ChillMCP server."""
    # Parse command-line arguments
    config = parse_args()

    # Create and run the server
    mcp = create_server(config)
    mcp.run()


if __name__ == "__main__":
    main()
