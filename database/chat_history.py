import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_DIR.mkdir(
    exist_ok=True
)

DB_PATH = DATABASE_DIR / "chat_history.db"


# ============================================================
# CONNECT DATABASE
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE TABLE
# ============================================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# SAVE CHAT
# ============================================================

def save_chat(
    user_message,
    ai_response
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (user_message, ai_response)
        VALUES (?, ?)
        """,
        (
            user_message,
            ai_response
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET CHAT HISTORY
# ============================================================

def get_chat_history(
    limit=50
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            user_message,
            ai_response,
            created_at
        FROM chat_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in reversed(rows)
    ]


# ============================================================
# CLEAR CHAT HISTORY
# ============================================================

def clear_chat_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM chat_history"
    )

    connection.commit()

    connection.close()


# ============================================================
# COUNT MESSAGES
# ============================================================

def get_chat_count():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM chat_history"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print(" ZENO CHAT HISTORY DATABASE TEST")
    print("=" * 55)

    # Create database/table
    init_database()

    print("\nDatabase:")
    print(DB_PATH)

    # Test save
    save_chat(
        "Hello ZENO",
        "Hello! How can I help you?"
    )

    # Test count
    print(
        "\nTotal chats:",
        get_chat_count()
    )

    # Test history
    print("\nChat history:")

    history = get_chat_history()

    for chat in history:

        print(
            f"\n[{chat['created_at']}]"
        )

        print(
            "You:",
            chat["user_message"]
        )

        print(
            "ZENO:",
            chat["ai_response"]
        )

    print("\n")
    print("CHAT HISTORY TEST SUCCESSFUL")