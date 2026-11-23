import os
import sqlite3
from contextlib import contextmanager

DATA_DIR = os.environ.get("DATA_DIR", "./data_volume")
DB_PATH = os.path.join(DATA_DIR, "event.db")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")


def init():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS olympic_scores (
                event_id TEXT NOT NULL,
                team TEXT NOT NULL,
                points INTEGER NOT NULL DEFAULT 0,
                note TEXT,
                PRIMARY KEY (event_id, team)
            );

            CREATE TABLE IF NOT EXISTS scavenger_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                team TEXT NOT NULL,
                points INTEGER NOT NULL,
                text_answer TEXT,
                proof_path TEXT,
                voided INTEGER NOT NULL DEFAULT 0,
                approved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS scavenger_bonuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team TEXT NOT NULL,
                label TEXT NOT NULL,
                points INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS showdown_results (
                showdown_id TEXT PRIMARY KEY,
                winner_team TEXT NOT NULL
            );
            """
        )
        try:
            conn.execute("ALTER TABLE scavenger_submissions ADD COLUMN approved INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # column already exists
        conn.commit()


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
