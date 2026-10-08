"""Database layer: only talks to SQLite."""
import os
import sqlite3
from contextlib import closing

# Path comes from an environment variable so Docker/EC2 can change it
DB_PATH = os.getenv("DB_PATH", "library.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us use row["title"]
    return conn


def init_db():
    """Create the books table if it does not exist."""
    with closing(get_connection()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT NOT NULL,
                author     TEXT NOT NULL,
                issued_to  TEXT,
                issue_date TEXT
            )
            """
        )
        conn.commit()
