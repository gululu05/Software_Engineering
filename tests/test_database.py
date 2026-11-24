from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

import pytest

from database import (
    connect_database,
    create_user,
    get_lessons,
    get_subject_preferences,
    init_database,
    save_lessons,
    update_subject_preferences,
)
from models import Lesson, SubjectPreferences


def test_init_database(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"

    init_database(db_path)

    assert db_path.exists()

    with closing(connect_database(db_path)) as connection:
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()

    assert ("users",) in tables
    assert ("subjects",) in tables
    assert ("lessons",) in tables
    assert ("subject_preferences",) in tables


def test_save_and_load_lessons(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_database(db_path)

    user_a = create_user("Student_A", db_path)
    user_b = create_user("Student_B", db_path)

    lesson = Lesson(
        event_id="test_event",
        subject_id="physik",
        subject_name="Physik",
        start=datetime(2026, 11, 25, 8, 15, tzinfo=UTC),
        end=datetime(2026, 11, 25, 9, 45, tzinfo=UTC),
    )

    save_lessons(user_a, [lesson], db_path)

    assert get_lessons(user_a, db_path) == [lesson]
    assert get_lessons(user_b, db_path) == []

    save_lessons(user_a, [lesson], db_path)

    assert len(get_lessons(user_a, db_path)) == 1


def test_subject_preferences(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_database(db_path)

    user_a = create_user("Student_A", db_path)
    user_b = create_user("Student_B", db_path)

    lesson = Lesson(
        event_id="event_1",
        subject_id="dynamik",
        subject_name="Dynamik",
        start=datetime(2026, 11, 25, 8, 15, tzinfo=UTC),
        end=datetime(2026, 11, 25, 9, 45, tzinfo=UTC),
    )

    save_lessons(user_a, [lesson], db_path)
    save_lessons(user_b, [lesson], db_path)

    assert get_subject_preferences(user_a, db_path) == [SubjectPreferences(subject_id="dynamik")]

    preferences = SubjectPreferences(
        subject_id="dynamik",
        importance=5,
        recorded=True,
        can_catch_up=False,
    )

    update_subject_preferences(user_a, preferences, db_path)

    assert get_subject_preferences(user_a, db_path) == [preferences]

    # Other users must not be affected.
    assert get_subject_preferences(user_b, db_path) == [SubjectPreferences(subject_id="dynamik")]

    # Importing the calendar again must preserve preferences.
    save_lessons(user_a, [lesson], db_path)

    assert get_subject_preferences(user_a, db_path) == [preferences]

    # Invalid importance ratings must be rejected.
    preferences.importance = 6

    with pytest.raises(ValueError, match="Importance"):
        update_subject_preferences(user_a, preferences, db_path)
