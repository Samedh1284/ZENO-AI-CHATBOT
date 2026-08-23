# ============================================================
# ZENO AI - MCP SERVER
# MCP 2.0 + CoinGecko
# ============================================================

import ast
import operator
import os
from datetime import datetime

import httpx

from mcp.server import MCPServer


# ============================================================
# MCP SERVER
# ============================================================

server = MCPServer(
    name="ZENO MCP Tools"
)


# ============================================================
# SAFE CALCULATOR
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_calculate(expression):

    def evaluate(node):

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):

                return node.value

            raise ValueError("Invalid value")

        if isinstance(node, ast.BinOp):

            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError("Operator not allowed")

            return operation(
                left,
                right
            )

        if isinstance(node, ast.UnaryOp):

            operation = OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError("Operator not allowed")

            return operation(
                evaluate(node.operand)
            )

        raise ValueError(
            "Invalid mathematical expression"
        )

    tree = ast.parse(
        expression,
        mode="eval"
    )

    return evaluate(tree.body)


# ============================================================
# TOOL 1 - ADD NUMBERS
# ============================================================

@server.tool()
async def add_numbers(
    a: float,
    b: float
):

    return {
        "result": float(a + b)
    }


# ============================================================
# TOOL 2 - MULTIPLY NUMBERS
# ============================================================

@server.tool()
async def multiply_numbers(
    a: float,
    b: float
):

    return {
        "result": float(a * b)
    }


# ============================================================
# TOOL 3 - CALCULATOR
# ============================================================

@server.tool()
async def calculator(
    expression: str
):

    try:

        result = safe_calculate(
            expression
        )

        return {
            "result": float(result)
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# TOOL 4 - CURRENT TIME
# ============================================================

@server.tool()
async def current_time():

    now = datetime.now()

    return {
        "result": now.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


# ============================================================
# TOOL 5 - COINGECKO CRYPTO PRICE
# ============================================================

@server.tool()
async def crypto_price(
    coin: str,
    currency: str = "usd"
):

    """
    Get current cryptocurrency price
    from CoinGecko.

    Examples:

    bitcoin
    ethereum
    solana

    currency:

    usd
    inr
    eur
    gbp
    """

    coin = coin.lower().strip()
    currency = currency.lower().strip()

    # --------------------------------------------------------
    # Common CoinGecko IDs
    # --------------------------------------------------------

    coin_aliases = {

        "btc": "bitcoin",
        "bitcoin": "bitcoin",

        "eth": "ethereum",
        "ethereum": "ethereum",

        "sol": "solana",
        "solana": "solana",

        "bnb": "binancecoin",
        "binance": "binancecoin",

        "xrp": "ripple",
        "ripple": "ripple",

        "doge": "dogecoin",
        "dogecoin": "dogecoin",

        "ada": "cardano",
        "cardano": "cardano",

        "dot": "polkadot",
        "polkadot": "polkadot",

        "matic": "matic-network",
        "polygon": "matic-network",

        "avax": "avalanche-2",
        "avalanche": "avalanche-2"
    }

    coin_id = coin_aliases.get(
        coin,
        coin
    )

    # --------------------------------------------------------
    # CoinGecko API
    # --------------------------------------------------------

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
    )

    params = {
        "ids": coin_id,
        "vs_currencies": currency,
        "include_24hr_change": "true",
        "include_market_cap": "true",
        "include_24hr_vol": "true"
    }

    # Optional API key
    api_key = os.getenv(
        "COINGECKO_API_KEY"
    )

    headers = {
        "accept": "application/json"
    }

    if api_key:

        headers[
            "x-cg-demo-api-key"
        ] = api_key

    # --------------------------------------------------------
    # Request
    # --------------------------------------------------------

    try:

        async with httpx.AsyncClient(
            timeout=15
        ) as client:

            response = await client.get(
                url,
                params=params,
                headers=headers
            )

        if response.status_code != 200:

            return {
                "error": (
                    f"CoinGecko API error "
                    f"{response.status_code}: "
                    f"{response.text}"
                )
            }

        data = response.json()

        # ----------------------------------------------------
        # Coin not found
        # ----------------------------------------------------

        if coin_id not in data:

            return {
                "error": (
                    f"Cryptocurrency '{coin}' "
                    "was not found."
                )
            }

        coin_data = data[
            coin_id
        ]

        price = coin_data.get(
            currency
        )

        change = coin_data.get(
            f"{currency}_24h_change"
        )

        market_cap = coin_data.get(
            f"{currency}_market_cap"
        )

        volume = coin_data.get(
            f"{currency}_24h_vol"
        )

        return {

            "coin": coin_id,

            "currency": currency,

            "price": price,

            "change_24h": change,

            "market_cap": market_cap,

            "volume_24h": volume
        }

    except Exception as e:

        return {
            "error": (
                "CoinGecko connection failed: "
                + str(e)
            )
        }


# ============================================================
# SERVER START
# ============================================================

if __name__ == "__main__":

    server.run()