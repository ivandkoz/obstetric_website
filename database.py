import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "survey.db"


def init_database():
    """Initialize db if it doesn't exist """

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                weeks INTEGER NOT NULL,
                premature_birth INTEGER NOT NULL,
                smokes INTEGER NOT NULL,
                adynamia INTEGER NOT NULL,
                smoothness INTEGER NOT NULL,
                wb_level INTEGER NOT NULL,
                bmi INTEGER NOT NULL,
                sti INTEGER NOT NULL,
                spotting INTEGER NOT NULL,

                probability REAL NOT NULL
            )
        """)


def save_response(answers, probability):
    """Save response to db"""

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute("""
            INSERT INTO responses (
                weeks,
                premature_birth,
                smokes,
                adynamia,
                smoothness,
                wb_level,
                bmi,
                sti,
                spotting,
                probability
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            answers["weeks"],
            answers["premature_birth"],
            answers["smokes"],
            answers["adynamia"],
            answers["smoothness"],
            answers["wb_level"],
            answers["bmi"],
            answers["sti"],
            answers["spotting"],
            probability
        ))

        return cursor.lastrowid