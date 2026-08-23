import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_PATH = PROJECT_ROOT / "mcp_server" / "server.py"


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)]
    )

    print("\nStarting MCP server...")

    async with Client(
        stdio_client(server_params)
    ) as client:

        # -----------------------------------------
        # List MCP tools
        # -----------------------------------------

        tools = await client.list_tools()

        print("\nAvailable MCP tools:")

        for tool in tools.tools:
            print("-", tool.name)

        # -----------------------------------------
        # Test current time
        # -----------------------------------------

        print("\nTesting current_time...")

        result = await client.call_tool(
            "current_time",
            {}
        )

        print("\nMCP result:")

        if result.structured_content:
            print(result.structured_content)

        if result.content:

            print("\nReadable result:")

            for content in result.content:

                if hasattr(content, "text"):
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())