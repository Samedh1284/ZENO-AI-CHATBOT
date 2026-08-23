# ============================================================
# ZENO AI API
# FastAPI -> ZENO AI -> MCP / RAG / Gemini
# + SQLite Chat History
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ai import ask_ai

from backend.chat_history import (
    init_db,
    save_chat,
    get_chat_history,
    clear_chat_history
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

init_db()


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ZENO AI API",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str


# ============================================================
# RESPONSE MODEL
# ============================================================

class ChatResponse(BaseModel):

    response: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
async def home():

    return {
        "status": "online",
        "name": "ZENO AI",
        "message": "ZENO AI API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


# ============================================================
# CHAT
# ============================================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:

        return ChatResponse(
            response="Please enter a message."
        )


    try:

        # ----------------------------------------------------
        # ASK ZENO AI
        # ----------------------------------------------------

        answer = await ask_ai(
            message
        )

        answer = str(answer)


        # ----------------------------------------------------
        # SAVE CHAT TO SQLITE
        # ----------------------------------------------------

        try:

            save_chat(
                message,
                answer
            )

            print(
                "[HISTORY] Chat saved successfully"
            )

        except Exception as history_error:

            print(
                "[HISTORY ERROR]",
                history_error
            )


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return ChatResponse(
            response=answer
        )


    except Exception as e:

        error_message = (
            "ZENO Error: "
            + str(e)
        )

        print(
            "[CHAT ERROR]",
            error_message
        )


        return ChatResponse(
            response=error_message
        )


# ============================================================
# GET CHAT HISTORY
# ============================================================

@app.get("/history")
async def history():

    try:

        chats = get_chat_history(
            limit=50
        )


        return {
            "success": True,
            "history": chats
        }


    except Exception as e:

        print(
            "[HISTORY GET ERROR]",
            e
        )


        return {
            "success": False,
            "history": [],
            "error": str(e)
        }


# ============================================================
# CLEAR CHAT HISTORY
# ============================================================

@app.delete("/history")
async def delete_history():

    try:

        clear_chat_history()


        return {
            "success": True,
            "message": "Chat history cleared"
        }


    except Exception as e:

        print(
            "[HISTORY DELETE ERROR]",
            e
        )


        return {
            "success": False,
            "message": "Unable to clear history",
            "error": str(e)
        }


# ============================================================
# TEST HISTORY
# ============================================================

@app.get("/history/test")
async def history_test():

    try:

        chats = get_chat_history(
            limit=5
        )


        return {
            "status": "working",
            "count": len(chats),
            "history": chats
        }


    except Exception as e:

        return {
            "status": "error",
            "error": str(e)
        }