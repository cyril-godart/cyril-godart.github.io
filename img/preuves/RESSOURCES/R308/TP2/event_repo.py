from __future__ import annotations
import json, pickle, os
from typing import List, Dict, Any
from events import Event
from datex import Date
from daterange import DateRange

class BaseEventRepository:
    def save(self, events: List[Event]) -> None: raise NotImplementedError
    def load(self) -> List[Event]: raise NotImplementedError

class EventJsonlRepository(BaseEventRepository):
    def __init__(self, path: str): self._path = path

    def save(self, events: List[Event]) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            for ev in events:
                rec = {
                    "title": ev.title,
                    "start": ev.period.start.to_iso(),
                    "end": ev.period.end.to_iso(),
                    "tags": ev.tags,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def load(self) -> List[Event]:
        out: List[Event] = []
        with open(self._path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                    title = rec["title"]
                    s = Date.from_iso(rec["start"])
                    e = Date.from_iso(rec["end"])
                    period = DateRange(s, e)
                    tags = rec.get("tags") or []
                    if not isinstance(tags, list):
                        raise ValueError("tags must be list")
                    out.append(Event(title, period, tags))
                except Exception as e:
                    raise ValueError(f"Line {i}: {e}") from e
        return out

class EventBinaryRepository(BaseEventRepository):
    def __init__(self, path: str): self._path = path

    def save(self, events: List[Event]) -> None:
        payload = [ (ev.title, ev.period.start.to_iso(), ev.period.end.to_iso(), list(ev.tags)) for ev in events ]
        with open(self._path, "wb") as f:
            pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self) -> List[Event]:
        with open(self._path, "rb") as f:
            payload = pickle.load(f)
        out: List[Event] = []
        for title, s, e, tags in payload:
            period = DateRange(Date.from_iso(s), Date.from_iso(e))
            out.append(Event(title, period, list(tags)))
        return out