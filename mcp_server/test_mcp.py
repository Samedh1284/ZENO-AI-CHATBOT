# ============================================================
# ZENO MCP 2.0 + COINGECKO TEST
# ============================================================

import asyncio
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import (
    StdioServerParameters,
    stdio_client
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SERVER_PATH = (
    PROJECT_ROOT
    / "mcp_server"
    / "server.py"
)


# ============================================================
# MAIN
# ============================================================

async def main():

    print("=" * 60)
    print(" ZENO MCP 2.0 + COINGECKO TEST")
    print("=" * 60)

    print()
    print("Python:")
    print(sys.executable)

    print()
    print("Server:")
    print(SERVER_PATH)

    print()
    print("Server exists:")
    print(SERVER_PATH.exists())

    # ========================================================
    # SERVER PARAMETERS
    # ========================================================

    server_params = StdioServerParameters(

        command=sys.executable,

        args=[
            str(SERVER_PATH)
        ],

        cwd=str(PROJECT_ROOT)
    )

    print()
    print("Connecting to MCP...")

    try:

        # ====================================================
        # MCP CONNECTION
        # ====================================================

        async with Client(
            stdio_client(server_params)
        ) as client:

            print()
            print("MCP CONNECTED!")

            # =================================================
            # LIST TOOLS
            # =================================================

            tools = await client.list_tools()

            print()
            print("Available MCP tools:")

            for tool in tools.tools:

                print(
                    " -",
                    tool.name
                )

            # =================================================
            # CURRENT TIME
            # =================================================

            print()
            print("Testing current_time...")

            result = await client.call_tool(
                "current_time",
                {}
            )

            print("Result:")
            print(result)

            # =================================================
            # CALCULATOR
            # =================================================

            print()
            print("Testing calculator...")

            result = await client.call_tool(
                "calculator",
                {
                    "expression": "25 + 30"
                }
            )

            print("Result:")
            print(result)

            # =================================================
            # ADD NUMBERS
            # =================================================

            print()
            print("Testing add_numbers...")

            result = await client.call_tool(
                "add_numbers",
                {
                    "a": 25,
                    "b": 40
                }
            )

            print("Result:")
            print(result)

            # =================================================
            # MULTIPLY NUMBERS
            # =================================================

            print()
            print("Testing multiply_numbers...")

            result = await client.call_tool(
                "multiply_numbers",
                {
                    "a": 10,
                    "b": 5
                }
            )

            print("Result:")
            print(result)

            # =================================================
            # COINGECKO
            # =================================================

            print()
            print("Testing crypto_price...")

            result = await client.call_tool(
                "crypto_price",
                {
                    "coin": "bitcoin",
                    "currency": "usd"
                }
            )

            print("Result:")
            print(result)

            # =================================================
            # SUCCESS
            # =================================================

            print()
            print("=" * 60)
            print(" MCP + COINGECKO TEST SUCCESSFUL")
            print("=" * 60)

    except Exception as e:

        print()
        print("=" * 60)
        print(" MCP TEST FAILED")
        print("=" * 60)

        print()
        print("Type:")
        print(type(e).__name__)

        print()
        print("Error:")
        print(str(e))


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())