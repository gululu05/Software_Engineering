"""Database management for StundenplanB."""

import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path

from models import Lesson, SubjectPreferences

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "stundenplanb.db"


def get_lessons(
    user_id: int,
    path: Path = DB_PATH,
) -> list[Lesson]:
    """Return all lessons belonging to a user."""
    with closing(connect_database(path)) as connection:
        rows = connection.execute(
            """
            SELECT l.event_id, l.subject_id, s.subject_name,
                   l.start, l.end, l.is_exam,
                   l.location, l.description
            FROM lessons AS l
            JOIN subjects AS s
                ON l.user_id = s.user_id
                AND l.subject_id = s.subject_id
            WHERE l.user_id = ?
            ORDER BY l.start
            """,
            (user_id,),
        ).fetchall()

    return [
        Lesson(
            event_id=row[0],
            subject_id=row[1],
            subject_name=row[2],
            start=datetime.fromisoformat(row[3]),
            end=datetime.fromisoformat(row[4]),
            is_exam=bool(row[5]),
            location=row[6],
            description=row[7],
        )
        for row in rows
    ]


def save_lessons(
    user_id: int,
    lessons: list[Lesson],
    path: Path = DB_PATH,
) -> None:
    """Save lessons and create missing subjects."""
    with closing(connect_database(path)) as connection, connection:
        for lesson in lessons:
            connection.execute(
                """
                INSERT INTO subjects (user_id, subject_id, subject_name)
                VALUES (?, ?, ?)
                ON CONFLICT (user_id, subject_id)
                DO UPDATE SET subject_name = excluded.subject_name
                """,
                (user_id, lesson.subject_id, lesson.subject_name),
            )

            connection.execute(
                """
                INSERT OR IGNORE INTO subject_preferences
                (user_id, subject_id)
                VALUES (?, ?)
                """,
                (user_id, lesson.subject_id),
            )

            connection.execute(
                """
                INSERT INTO lessons
                (user_id, event_id, subject_id, start, end,
                 is_exam, location, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (user_id, event_id)
                DO UPDATE SET
                    subject_id = excluded.subject_id,
                    start = excluded.start,
                    end = excluded.end,
                    is_exam = excluded.is_exam,
                    location = excluded.location,
                    description = excluded.description
                """,
                (
                    user_id,
                    lesson.event_id,
                    lesson.subject_id,
                    lesson.start.isoformat(),
                    lesson.end.isoformat(),
                    lesson.is_exam,
                    lesson.location,
                    lesson.description,
                ),
            )


def connect_database(
    path: Path = DB_PATH,
) -> sqlite3.Connection:
    """Connect to the SQLite database."""
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database(path: Path = DB_PATH) -> None:
    """Create the database and its tables."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with closing(connect_database(path)) as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS subjects (
                user_id INTEGER NOT NULL,
                subject_id TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                PRIMARY KEY (user_id, subject_id),
                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS lessons (
                user_id INTEGER NOT NULL,
                event_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                start TEXT NOT NULL,
                end TEXT NOT NULL,
                is_exam INTEGER NOT NULL DEFAULT 0
                    CHECK (is_exam IN (0, 1)),
                location TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (user_id, event_id),
                FOREIGN KEY (user_id, subject_id)
                    REFERENCES subjects(user_id, subject_id)
            );

            CREATE TABLE IF NOT EXISTS subject_preferences (
                user_id INTEGER NOT NULL,
                subject_id TEXT NOT NULL,
                importance INTEGER
                    CHECK (importance IN (1, 2, 3, 4, 5)),
                recorded INTEGER
                    CHECK (recorded IN (0, 1)),
                can_catch_up INTEGER
                    CHECK (can_catch_up IN (0, 1)),
                PRIMARY KEY (user_id, subject_id),
                FOREIGN KEY (user_id, subject_id)
                    REFERENCES subjects(user_id, subject_id)
            );
        """)
        connection.commit()


def create_user(username: str, path: Path = DB_PATH) -> int:
    """Create a user and return the user ID."""
    with closing(connect_database(path)) as connection:
        cursor = connection.execute(
            "INSERT INTO users (username) VALUES (?)",
            (username,),
        )
        connection.commit()

        user_id = cursor.lastrowid

        if user_id is None:
            raise RuntimeError("User creation failed.")

        return user_id


def get_subject_preferences(
    user_id: int,
    path: Path = DB_PATH,
) -> list[SubjectPreferences]:
    """Return all subject preferences belonging to a user."""
    with closing(connect_database(path)) as connection:
        rows = connection.execute(
            """
            SELECT subject_id, importance, recorded, can_catch_up
            FROM subject_preferences
            WHERE user_id = ?
            ORDER BY subject_id
            """,
            (user_id,),
        ).fetchall()

    return [
        SubjectPreferences(
            subject_id=row[0],
            importance=row[1],
            recorded=None if row[2] is None else bool(row[2]),
            can_catch_up=None if row[3] is None else bool(row[3]),
        )
        for row in rows
    ]


def update_subject_preferences(
    user_id: int,
    preferences: SubjectPreferences,
    path: Path = DB_PATH,
) -> None:
    """Update personal preferences for a subject."""
    importance = preferences.importance

    if importance is not None and (
        not isinstance(importance, int) or isinstance(importance, bool) or not 1 <= importance <= 5
    ):
        raise ValueError("Importance must be between 1 and 5.")

    with closing(connect_database(path)) as connection, connection:
        cursor = connection.execute(
            """
            UPDATE subject_preferences
            SET importance = ?, recorded = ?, can_catch_up = ?
            WHERE user_id = ? AND subject_id = ?
            """,
            (
                preferences.importance,
                preferences.recorded,
                preferences.can_catch_up,
                user_id,
                preferences.subject_id,
            ),
        )

        if cursor.rowcount == 0:
            raise ValueError("Subject not found.")


if __name__ == "__main__":
    init_database()
