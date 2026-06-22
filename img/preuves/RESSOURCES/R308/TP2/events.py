from __future__ import annotations
from typing import List
from daterange import DateRange

class Event:
    __slots__ = ("title", "period", "tags")

    def __init__(self, title: str, period: DateRange, tags: List[str] | None = None):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(period, DateRange):
            raise TypeError("period must be a DateRange")
        self.title = title.strip()
        self.period = period
        self.tags = list(tags) if tags else []

    def overlaps(self, other: "Event") -> bool:
        return self.period.overlaps(other.period)

    def __repr__(self) -> str:
        return f"Event({self.title!r}, [{self.period.start.to_iso()}..{self.period.end.to_iso()}], tags={self.tags!r})"

    def __str__(self) -> str:
        return f"{self.title} [{self.period.start.to_iso()}..{self.period.end.to_iso()}] tags={self.tags}"