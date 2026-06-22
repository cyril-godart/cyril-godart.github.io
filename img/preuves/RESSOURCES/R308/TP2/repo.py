from __future__ import annotations
import json
from typing import List, Dict, Any
from datex import Date
from daterange import DateRange
from errors import InvalidDateError, DateParseError

class RepositoryError(Exception): ...
class RepositoryIOError(RepositoryError): ...
class RepositoryDataError(RepositoryError): ...

class DateRangeRepository:
    def __init__(self, path: str):
        self._path = path

    def save(self, ranges: List[DateRange]) -> None:
        try:
            print(f"[INFO] Saving {len(ranges)} ranges to {self._path}")
            with open(self._path, "w", encoding="utf-8") as f:
                for r in ranges:
                    rec = {"start": r.start.to_iso(), "end": r.end.to_iso()}
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except OSError as e:
            raise RepositoryIOError(f"I/O error while writing {self._path}: {e}") from e

    def load(self) -> List[DateRange]:
        out: List[DateRange] = []
        try:
            print(f"[INFO] Loading ranges from {self._path}")
            with open(self._path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        rec = json.loads(line)
                        s = rec.get("start"); e = rec.get("end")
                        if not (isinstance(s, str) and isinstance(e, str)):
                            raise RepositoryDataError(f"Line {i}: missing 'start'/'end' strings")
                        ds = Date.from_iso(s)
                        de = Date.from_iso(e)
                        if de < ds:
                            raise RepositoryDataError(f"Line {i}: end < start ({e} < {s})")
                        out.append(DateRange(ds, de))
                    except RepositoryDataError:
                        raise
                    except (InvalidDateError, DateParseError) as e2:
                        raise RepositoryDataError(f"Line {i}: {e2}") from e2
                    except Exception as e3:
                        raise RepositoryDataError(f"Line {i}: invalid record: {e3}") from e3
        except OSError as e:
            raise RepositoryIOError(f"I/O error while reading {self._path}: {e}") from e
        return out

# --- Quick self-test ---
if __name__ == "__main__":
    repo = DateRangeRepository("ranges.jsonl")
    a = DateRange(Date(2025, 9, 1), Date(2025, 9, 10))
    b = DateRange(Date(2025, 9, 20), Date(2025, 9, 21))
    repo.save([a, b])
    loaded = repo.load()
    assert len(loaded) == 2 and loaded[0].start.to_iso() == "2025-09-01"
    print("Tests Ex4 OK")