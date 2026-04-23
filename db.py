import sqlite3
import json
from datetime import datetime

DB_NAME = "history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS subtitle_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            timestamp TEXT,
            report TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_report(filename, report):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO subtitle_history (filename, timestamp, report)
        VALUES (?, ?, ?)
    """, (
        filename,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        json.dumps(report)
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT filename, timestamp, report FROM subtitle_history ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    return rows