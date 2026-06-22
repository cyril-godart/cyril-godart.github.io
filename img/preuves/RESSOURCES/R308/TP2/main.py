from __future__ import annotations
from events import Event
from daterange import DateRange
from datex import Date
from event_repo import EventJsonlRepository, EventBinaryRepository

def any_overlaps(events):
    n = len(events)
    conflicts = []
    for i in range(n):
        for j in range(i+1, n):
            if events[i].overlaps(events[j]):
                conflicts.append((events[i].title, events[j].title))
    return conflicts

if __name__ == "__main__":
    evs = [
        Event("Conf IAG", DateRange(Date(2025,10,6), Date(2025,10,6)), ["univ","iag"]),
        Event("Soutenance", DateRange(Date(2025,11,3), Date(2025,11,3)), ["phd"]),
        Event("Vacances Toussaint", DateRange(Date(2025,10,25), Date(2025,11,2)), ["feries"]),
        Event("Jury", DateRange(Date(2025,11,2), Date(2025,11,2)), ["jury"]),
        Event("Formation IA", DateRange(Date(2025,10,30), Date(2025,10,30)), ["ia","formation"]),
    ]

    # Save & load JSONL
    json_repo = EventJsonlRepository("events.jsonl")
    json_repo.save(evs)
    evs_json = json_repo.load()

    # Save & load Binary
    bin_repo = EventBinaryRepository("events.pkl")
    bin_repo.save(evs)
    evs_bin = bin_repo.load()

    assert len(evs_json) == len(evs) == len(evs_bin)

    conflicts = any_overlaps(evs_json)
    print("Conflicts:", conflicts)

    import os
    sizes = {"events.jsonl": os.path.getsize("events.jsonl"), "events.pkl": os.path.getsize("events.pkl")}
    print("Sizes (bytes):", sizes)
    print("Text is human-readable and portable; binary is compact/fast but less transparent/interoperable.")