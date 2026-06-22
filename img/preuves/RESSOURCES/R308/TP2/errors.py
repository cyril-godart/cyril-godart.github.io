# errors.py
class DateError(Exception):
    """Base error for Date-related issues."""

class InvalidDateError(DateError):
    """Raised when a Date has invalid fields (year/month/day or impossible date)."""

class DateParseError(DateError):
    """Raised when parsing a Date (e.g., wrong format or invalid numbers)."""