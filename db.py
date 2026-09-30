import os
import psycopg

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5440/docuchat")

def init_db():
    with psycopg.connect(DB_URL) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            )""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_history(session_id)")

def save_message(session_id: str, role: str, content: str):
    with psycopg.connect(DB_URL) as conn:
        conn.execute(
            "INSERT INTO chat_history (session_id, role, content) VALUES (%s, %s, %s)",
            (session_id, role, content),   # parameter terpisah = aman dari SQL injection
        )

def get_history(session_id: str) -> list:
    with psycopg.connect(DB_URL) as conn:
        rows = conn.execute(
            "SELECT role, content, created_at FROM chat_history WHERE session_id = %s ORDER BY created_at",
            (session_id,),
        ).fetchall()
    return [{"role": r[0], "content": r[1], "created_at": r[2].isoformat()} for r in rows]