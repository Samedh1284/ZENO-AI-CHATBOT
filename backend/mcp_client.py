import asyncio
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters, stdio_client


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SERVER_PATH = PROJECT_ROOT / "mcp_server" / "server.py"


# ============================================================
# MCP TOOL CALL
# ============================================================

async def call_mcp_tool(tool_name, arguments=None):

    if arguments is None:
        arguments = {}

    print("[MCP] Connecting to server...")
    print(f"[MCP] Tool: {tool_name}")

    if not SERVER_PATH.exists():

        raise FileNotFoundError(
            f"MCP server not found:\n{SERVER_PATH}"
        )

    # --------------------------------------------------------
    # MCP SERVER PARAMETERS
    # --------------------------------------------------------

    server_params = StdioServerParameters(

        command=sys.executable,

        args=[
            str(SERVER_PATH)
        ],

        cwd=str(PROJECT_ROOT)

    )

    # --------------------------------------------------------
    # IMPORTANT:
    # stdio_client(...) creates the transport.
    #
    # Client(...) receives the transport.
    # --------------------------------------------------------

    try:

        async with Client(
            stdio_client(server_params)
        ) as client:

            print("[MCP] Connected")

            # ------------------------------------------------
            # LIST TOOLS
            # ------------------------------------------------

            tools_result = await client.list_tools()

            tools = tools_result.tools

            tool_names = [
                tool.name
                for tool in tools
            ]

            print(
                "[MCP] Available tools:",
                tool_names
            )

            # ------------------------------------------------
            # CHECK TOOL
            # ------------------------------------------------

            if tool_name not in tool_names:

                raise RuntimeError(
                    f"MCP tool '{tool_name}' not found.\n"
                    f"Available tools: {tool_names}"
                )

            # ------------------------------------------------
            # CALL TOOL
            # ------------------------------------------------

            result = await client.call_tool(
                tool_name,
                arguments
            )

            print("[MCP] Tool executed")

            # ------------------------------------------------
            # STRUCTURED RESULT
            # ------------------------------------------------

            structured = getattr(
                result,
                "structured_content",
                None
            )

            if isinstance(
                structured,
                dict
            ):

                if "result" in structured:

                    return {
                        "result":
                            structured["result"]
                    }

                return structured

            # ------------------------------------------------
            # TEXT RESULT
            # ------------------------------------------------

            content = getattr(
                result,
                "content",
                []
            )

            for item in content:

                text = getattr(
                    item,
                    "text",
                    None
                )

                if text is not None:

                    return {
                        "result": text
                    }

            # ------------------------------------------------
            # FALLBACK
            # ------------------------------------------------

            return {
                "result": str(result)
            }

    except Exception as e:

        print(
            f"[MCP ERROR] {type(e).__name__}: {e}"
        )

        raise


# ============================================================
# SYNCHRONOUS HELPER
# ============================================================

def call_mcp_tool_sync(
    tool_name,
    arguments=None
):

    return asyncio.run(
        call_mcp_tool(
            tool_name,
            arguments
        )
    )


# ============================================================
# TEST
# ============================================================

async def test_mcp():

    print("=" * 55)

    print(
        " ZENO MCP CLIENT TEST"
    )

    print("=" * 55)

    print(
        "\nServer:"
    )

    print(
        SERVER_PATH
    )

    print(
        "\nTesting current_time..."
    )

    result = await call_mcp_tool(
        "current_time",
        {}
    )

    print(
        "\nRESULT:"
    )

    print(
        result
    )


if __name__ == "__main__":

    asyncio.run(
        test_mcp()
    )