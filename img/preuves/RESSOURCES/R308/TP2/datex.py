from __future__ import annotations
from functools import total_ordering
import re
from errors import InvalidDateError, DateParseError

@total_ordering
class Date:
    """Minimal proleptic Gregorian date (immutable in practice)."""
    __slots__ = ("_y", "_m", "_d")

    def __init__(self, year: int, month: int, day: int):
        if not (isinstance(year, int) and isinstance(month, int) and isinstance(day, int)):
            raise InvalidDateError("year, month, day must be integers")
        if not (1 <= year <= 9999):
            raise InvalidDateError(f"year out of range: {year}")
        if not (1 <= month <= 12):
            raise InvalidDateError(f"month out of range: {month}")
        dim = self._days_in_month(year, month)
        if not (1 <= day <= dim):
            raise InvalidDateError(f"day out of range for {year:04d}-{month:02d}: {day}")
        object.__setattr__(self, "_y", year)
        object.__setattr__(self, "_m", month)
        object.__setattr__(self, "_d", day)

    @property
    def year(self) -> int: return self._y
    @property
    def month(self) -> int: return self._m
    @property
    def day(self) -> int: return self._d

    # --- Representations ---
    def __repr__(self) -> str:
        return f"Date({self._y:04d},{self._m:02d},{self._d:02d})"

    def __str__(self) -> str:
        return f"{self._y:04d}-{self._m:02d}-{self._d:02d}"

    def to_iso(self) -> str:
        return str(self)

    @classmethod
    def from_iso(cls, s: str) -> "Date":
        if not isinstance(s, str):
            raise DateParseError("expected string in YYYY-MM-DD")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
            raise DateParseError(f"invalid date format: {s!r}")
        y, m, d = (int(s[0:4]), int(s[5:7]), int(s[8:10]))
        try:
            return cls(y, m, d)
        except InvalidDateError as e:
            raise DateParseError(str(e)) from e

    # --- Calendrical helpers ---
    def is_leap_year(self) -> bool:
        y = self._y
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

    @staticmethod
    def _is_leap(y: int) -> bool:
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

    @staticmethod
    def _days_in_month(y: int, m: int) -> int:
        if m == 2:
            return 29 if Date._is_leap(y) else 28
        if m in (1,3,5,7,8,10,12):
            return 31
        return 30

    def day_of_year(self) -> int:
        mdays = [31, 29 if self.is_leap_year() else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return sum(mdays[:self._m-1]) + self._d

    # Ordinal: days since 0001-01-01 (ordinal 1 == 0001-01-01)
    def _to_ordinal(self) -> int:
        y = self._y
        # Days in previous years
        y1 = y - 1
        leaps = y1//4 - y1//100 + y1//400
        days_prev_years = y1*365 + leaps
        # Days in previous months this year
        days_prev_months = 0
        for m in range(1, self._m):
            days_prev_months += Date._days_in_month(y, m)
        return days_prev_years + days_prev_months + self._d

    @classmethod
    def _from_ordinal(cls, n: int) -> "Date":
        if n < 1:
            raise InvalidDateError("ordinal must be >= 1")
        # Find year via incremental search (binary-ish on centuries could be added; linear is fine here)
        # Use an efficient approach: estimate year
        # upper bound rough
        y = (n * 400) // 146097 + 1  # 146097 days in 400-year cycle
        # Adjust downward if needed
        def days_before_year(yy: int) -> int:
            y1 = yy - 1
            return y1*365 + (y1//4 - y1//100 + y1//400)
        # Correct y
        while days_before_year(y+1) < n:
            y += 1
        while days_before_year(y) >= n:
            y -= 1
        day_of_year = n - days_before_year(y)
        # Find month
        m = 1
        while True:
            dim = Date._days_in_month(y, m)
            if day_of_year > dim:
                day_of_year -= dim
                m += 1
            else:
                d = day_of_year
                break
        return cls(y, m, d)

    def add_days(self, n: int) -> "Date":
        if not isinstance(n, int):
            raise TypeError("n must be int")
        ordn = self._to_ordinal() + n
        return self._from_ordinal(ordn)

    # --- Ordering ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return (self._y, self._m, self._d) == (other._y, other._m, other._d)

    def __lt__(self, other: "Date") -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return (self._y, self._m, self._d) < (other._y, other._m, other._d)

# --- Quick self-test ---
if __name__ == "__main__":
    d = Date(2024, 2, 29)
    assert d.is_leap_year() is True
    assert str(d) == "2024-02-29"
    assert Date.from_iso("2025-09-22").to_iso() == "2025-09-22"
    try:
        Date(2023, 2, 29)
        assert False, "Should raise InvalidDateError"
    except InvalidDateError:
        pass
    try:
        Date.from_iso("2025-13-01")
        assert False, "Should raise DateParseError"
    except DateParseError:
        pass
    d1 = Date(2025, 12, 31).add_days(1)
    assert str(d1) == "2026-01-01"
    assert Date(2025, 1, 1) < Date(2025, 1, 2)
    print("Tests Ex1 OK")