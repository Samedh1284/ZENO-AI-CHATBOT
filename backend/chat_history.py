import sqlite3
from pathlib import Path


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chatbot.db"


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# SAVE CHAT
# ============================================================

def save_chat(user_message, bot_response):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (user_message, bot_response)
        VALUES (?, ?)
    """, (
        user_message,
        bot_response
    ))

    conn.commit()
    conn.close()


# ============================================================
# GET CHAT HISTORY
# ============================================================

def get_chat_history(limit=50):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            user_message,
            bot_response,
            created_at
        FROM chat_history
        ORDER BY id ASC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "user_message": row[1],
            "bot_response": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]


# ============================================================
# DELETE HISTORY
# ============================================================

def clear_chat_history():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM chat_history")

    conn.commit()
    conn.close()


# ============================================================
# START DATABASE
# ============================================================

init_db()