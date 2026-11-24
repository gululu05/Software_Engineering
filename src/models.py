"""Shared data models for StundenplanB."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lesson:
    """Represent a scheduled lesson."""

    event_id: str
    subject_id: str
    subject_name: str
    start: datetime
    end: datetime
    is_exam: bool = False
    location: str = ""
    description: str = ""


@dataclass
class SubjectPreferences:
    """Represent personal subject preferences."""

    subject_id: str
    importance: int | None = None
    recorded: bool | None = None
    can_catch_up: bool | None = None
