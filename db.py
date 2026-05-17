import sqlite3
from datetime import datetime, timezone

DB_PATH = "leads.db"


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                phone       TEXT UNIQUE NOT NULL,
                category    TEXT,
                messaged    INTEGER DEFAULT 0,
                messaged_at TEXT
            )
        """)


def insert_lead(name: str, phone: str, category: str) -> bool:
    """Returns True if inserted, False if phone already existed."""
    with _conn() as con:
        cur = con.execute(
            "INSERT OR IGNORE INTO leads (name, phone, category) VALUES (?, ?, ?)",
            (name, phone, category),
        )
        return cur.rowcount == 1


def get_unsent_leads(limit: int = 5) -> list[dict]:
    with _conn() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT id, name, phone, category FROM leads WHERE messaged = 0 LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def mark_messaged(phone: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as con:
        con.execute(
            "UPDATE leads SET messaged = 1, messaged_at = ? WHERE phone = ?",
            (now, phone),
        )
