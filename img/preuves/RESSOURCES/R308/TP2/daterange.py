from __future__ import annotations
from datex import Date, InvalidDateError

class DateRange:
    __slots__ = ("start", "end")

    def __init__(self, start: Date, end: Date):
        if not isinstance(start, Date) or not isinstance(end, Date):
            raise InvalidDateError("start and end must be Date instances")
        if end < start:
            raise InvalidDateError("end must be >= start")
        self.start = start
        self.end = end

    def duration(self) -> int:
        # inclusive duration in days
        return (self.end._to_ordinal() - self.start._to_ordinal()) + 1

    def contains(self, d: Date) -> bool:
        return self.start <= d <= self.end

    def overlaps(self, other: "DateRange") -> bool:
        return not (self.end < other.start or other.end < self.start)

    def intersection(self, other: "DateRange") -> "DateRange | None":
        if not self.overlaps(other):
            return None
        s = self.start if self.start >= other.start else other.start
        e = self.end if self.end <= other.end else other.end
        return DateRange(s, e)

# --- Quick self-test ---
if __name__ == "__main__":
    a = DateRange(Date(2025, 9, 1), Date(2025, 9, 10))
    b = DateRange(Date(2025, 9, 5), Date(2025, 9, 15))
    c = a.intersection(b)
    assert c is not None and c.start.to_iso() == "2025-09-05" and c.end.to_iso() == "2025-09-10"
    assert a.duration() == 10
    assert a.contains(Date(2025, 9, 1)) and a.contains(Date(2025, 9, 10))
    print("Tests Ex2 OK")