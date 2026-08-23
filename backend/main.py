from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.ai import ask_gemini


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title="ZENO AI",
    description="ZENO AI Chatbot Backend",
    version="1.0.0"
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
# Home
# ============================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "message": "ZENO AI backend is working!"
    }


# ============================================================
# Chat
# ============================================================

@app.get("/chat")
async def chat(message: str):

    message = message.strip()

    if not message:

        return {
            "success": False,
            "error": "Please enter a message."
        }

    try:

        answer = ask_gemini(message)

        return {
            "success": True,
            "user": message,
            "bot": answer
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }