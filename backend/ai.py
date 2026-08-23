# ============================================================
# ZENO AI
# MCP + RAG + COINGECKO + GEMINI
# ============================================================

import sys
import asyncio
import os
import json
import re
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from dotenv import load_dotenv
from google import genai

# IMPORTANT:
# mcp_client.py is inside backend/
from backend.mcp_client import call_mcp_tool

from rag.search import search


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# ============================================================
# GEMINI SETUP
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# NORMAL GEMINI
# ============================================================

async def ask_gemini(question):

    print("\n[Gemini] Normal AI question...")

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )

        return response.text

    except Exception as e:

        return (
            "Gemini Error:\n"
            + str(e)
        )


# ============================================================
# CALCULATOR DETECTOR
# ============================================================

def is_calculation(question):

    question = question.lower().strip()

    prefixes = [
        "calculate ",
        "what is ",
        "solve ",
        "compute "
    ]

    allowed = "0123456789+-*/(). %"

    for prefix in prefixes:

        if question.startswith(prefix):

            expression = question[
                len(prefix):
            ].strip()

            if expression and all(
                char in allowed
                for char in expression
            ):

                if any(
                    char.isdigit()
                    for char in expression
                ):
                    return expression

    # Direct calculation
    if question and all(
        char in allowed
        for char in question
    ):

        if any(
            char.isdigit()
            for char in question
        ):
            return question

    return None


# ============================================================
# TIME DETECTOR
# ============================================================

def is_time_question(question):

    question = question.lower()

    keywords = [

        "current time",
        "what time is it",
        "time now",
        "time right now",

        "current date",
        "today's date",
        "date today",

        "what is the date",
        "what's the date"

    ]

    return any(
        keyword in question
        for keyword in keywords
    )


# ============================================================
# ADDITION DETECTOR
# ============================================================

def detect_addition(question):

    question = (
        question
        .lower()
        .strip()
    )

    if question.startswith("add "):

        expression = question[4:].strip()

        parts = expression.split()

        if (
            len(parts) == 3
            and parts[1] == "+"
        ):

            try:

                return (
                    float(parts[0]),
                    float(parts[2])
                )

            except ValueError:
                pass

    return None


# ============================================================
# MULTIPLICATION DETECTOR
# ============================================================

def detect_multiplication(question):

    question = (
        question
        .lower()
        .strip()
    )

    if question.startswith("multiply "):

        expression = question[9:].strip()

        parts = expression.split()

        if (
            len(parts) == 3
            and parts[1] in ["*", "x"]
        ):

            try:

                return (
                    float(parts[0]),
                    float(parts[2])
                )

            except ValueError:
                pass

    return None


# ============================================================
# CRYPTO DETECTOR
# ============================================================

def detect_crypto(question):

    question = (
        question
        .lower()
        .strip()
    )

    crypto_words = [

        "bitcoin",
        "btc",

        "ethereum",
        "eth",

        "dogecoin",
        "doge",

        "solana",

        "xrp",

        "cardano",
        "ada",

        "bnb",

        "shiba",
        "shib"

    ]

    price_words = [

        "price",
        "value",
        "worth",
        "cost",

        "current",
        "live",

        "rate"

    ]

    has_crypto = any(
        word in question
        for word in crypto_words
    )

    has_price = any(
        word in question
        for word in price_words
    )

    if not has_crypto:
        return None

    if has_price or "how much" in question:

        if (
            "bitcoin" in question
            or "btc" in question
        ):
            return "bitcoin"

        if (
            "ethereum" in question
            or "eth" in question
        ):
            return "ethereum"

        if (
            "dogecoin" in question
            or "doge" in question
        ):
            return "dogecoin"

        if "solana" in question:
            return "solana"

        if "xrp" in question:
            return "ripple"

        if (
            "cardano" in question
            or "ada" in question
        ):
            return "cardano"

        if "bnb" in question:
            return "binancecoin"

        if (
            "shiba" in question
            or "shib" in question
        ):
            return "shiba-inu"

    return None


# ============================================================
# RAG DETECTOR
# ============================================================

def is_rag_question(question):

    question = question.lower()

    keywords = [

        "my skills",
        "my skill",

        "my resume",
        "my cv",

        "my education",
        "my qualification",

        "my experience",

        "my project",
        "my projects",

        "my internship",

        "my profile",

        "samedh skills",
        "samedh skill",

        "samedh resume",

        "samedh education",

        "samedh experience",

        "samedh project",

        "according to the document",

        "according to my resume",

        "from my resume",

        "from the document",

        "in the document",

        "in my document",

        "what does the document say"

    ]

    return any(
        keyword in question
        for keyword in keywords
    )


# ============================================================
# RAG
# ============================================================

async def ask_rag(question):

    print("\n[RAG] Searching document...")

    try:

        results = search(question)

        if not results:

            return (
                "I could not find relevant "
                "information in your documents."
            )

        print(
            f"[RAG] Found "
            f"{len(results)} relevant chunks."
        )

        context_parts = []

        for item in results:

            text = item.get("text", "")

            if text:
                context_parts.append(text)

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are ZENO AI.

Answer the user's question using ONLY
the information from the document context.

Do not invent information.

If the answer is not available in the
document, say that it is not available
in the document.

Give a clear and concise answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

        print(
            "[RAG] Generating answer..."
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        print("[RAG ERROR]")

        return (
            "RAG Error:\n"
            + str(e)
        )


# ============================================================
# FORMAT MCP RESULT
# ============================================================

def format_result(result):

    if result is None:
        return "No result returned."

    if isinstance(result, dict):

        if "result" in result:

            value = result["result"]

            if isinstance(
                value,
                (dict, list)
            ):

                return json.dumps(
                    value,
                    indent=2
                )

            return str(value)

        return json.dumps(
            result,
            indent=2
        )

    return str(result)


# ============================================================
# MAIN AI
# ============================================================

async def ask_ai(question):

    question = question.strip()

    if not question:

        return "Please enter a question."


    # ========================================================
    # COINGECKO / CRYPTO
    # ========================================================

    coin = detect_crypto(question)

    if coin:

        print("\n[MCP] crypto_price")
        print(f"[MCP] Coin: {coin}")

        try:

            result = await call_mcp_tool(
                "crypto_price",
                {
                    "coin": coin,
                    "currency": "usd"
                }
            )

            return format_result(result)

        except Exception as e:

            return (
                "Crypto MCP Error:\n"
                + str(e)
            )


    # ========================================================
    # CURRENT TIME
    # ========================================================

    if is_time_question(question):

        print("\n[MCP] current_time")

        try:

            result = await call_mcp_tool(
                "current_time",
                {}
            )

            return (
                "Current date and time: "
                + format_result(result)
            )

        except Exception as e:

            return (
                "Time MCP Error:\n"
                + str(e)
            )


    # ========================================================
    # CALCULATOR
    # ========================================================

    expression = is_calculation(question)

    if expression:

        print("\n[MCP] calculator")

        try:

            result = await call_mcp_tool(
                "calculator",
                {
                    "expression": expression
                }
            )

            return (
                "Answer: "
                + format_result(result)
            )

        except Exception as e:

            return (
                "Calculator MCP Error:\n"
                + str(e)
            )


    # ========================================================
    # ADD NUMBERS
    # ========================================================

    addition = detect_addition(question)

    if addition:

        a, b = addition

        print("\n[MCP] add_numbers")

        try:

            result = await call_mcp_tool(
                "add_numbers",
                {
                    "a": a,
                    "b": b
                }
            )

            return (
                "Answer: "
                + format_result(result)
            )

        except Exception as e:

            return (
                "Addition MCP Error:\n"
                + str(e)
            )


    # ========================================================
    # MULTIPLY NUMBERS
    # ========================================================

    multiplication = detect_multiplication(
        question
    )

    if multiplication:

        a, b = multiplication

        print("\n[MCP] multiply_numbers")

        try:

            result = await call_mcp_tool(
                "multiply_numbers",
                {
                    "a": a,
                    "b": b
                }
            )

            return (
                "Answer: "
                + format_result(result)
            )

        except Exception as e:

            return (
                "Multiplication MCP Error:\n"
                + str(e)
            )


    # ========================================================
    # RAG
    # ========================================================

    if is_rag_question(question):

        return await ask_rag(question)


    # ========================================================
    # GEMINI
    # ========================================================

    return await ask_gemini(question)


# ============================================================
# TERMINAL TEST
# ============================================================

async def main():

    print("=" * 60)

    print(
        " ZENO AI + MCP + RAG + COINGECKO"
    )

    print("=" * 60)

    while True:

        try:

            question = input(
                "\nYou: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print(
                "\nZENO: Goodbye!"
            )

            break

        if question.lower() in [
            "exit",
            "quit",
            "bye"
        ]:

            print(
                "\nZENO: Goodbye!"
            )

            break

        try:

            answer = await ask_ai(
                question
            )

            print("\nZENO:")
            print(answer)

        except Exception as e:

            print("\nERROR:")
            print(
                type(e).__name__
            )

            print(str(e))


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())