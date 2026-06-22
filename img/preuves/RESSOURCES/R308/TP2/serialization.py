from __future__ import annotations
import json, csv, pickle, os
from typing import Iterable, List
from datex import Date
from errors import DateParseError

def dump_dates_jsonl(dates: Iterable[Date], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for d in dates:
            rec = {"year": d.year, "month": d.month, "day": d.day}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def load_dates_jsonl(path: str) -> List[Date]:
    out: List[Date] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                y, m, d = int(rec["year"]), int(rec["month"]), int(rec["day"])
                out.append(Date(y, m, d))
            except Exception as e:
                raise DateParseError(f"JSONL line {i}: {e}") from e
    return out

def dump_dates_csv(dates: Iterable[Date], path: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "month", "day"])
        for d in dates:
            w.writerow([d.year, d.month, d.day])

def load_dates_csv(path: str) -> List[Date]:
    out: List[Date] = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for i, rec in enumerate(r, 2):  # header is line 1
            try:
                y, m, d = int(rec["year"]), int(rec["month"]), int(rec["day"])
                out.append(Date(y, m, d))
            except Exception as e:
                raise DateParseError(f"CSV line {i}: {e}") from e
    return out

def dump_dates_pickle(dates: Iterable[Date], path: str) -> None:
    with open(path, "wb") as f:
        # store as list of tuples to be robust to class changes
        payload = [(d.year, d.month, d.day) for d in dates]
        pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_dates_pickle(path: str) -> List[Date]:
    with open(path, "rb") as f:
        payload = pickle.load(f)
        out = []
        try:
            for y, m, d in payload:
                out.append(Date(int(y), int(m), int(d)))
        except Exception as e:
            raise DateParseError(f"Pickle payload invalid: {e}") from e
        return out

# --- Tests/bench ---
if __name__ == "__main__":
    base = Date(2025, 1, 1)
    dates = [base.add_days(i) for i in range(10000)]
    dump_dates_jsonl(dates, "dates.jsonl")
    dump_dates_csv(dates, "dates.csv")
    dump_dates_pickle(dates, "dates.pkl")
    lj = load_dates_jsonl("dates.jsonl")
    lc = load_dates_csv("dates.csv")
    lp = load_dates_pickle("dates.pkl")
    assert lj[:3][0].to_iso() == "2025-01-01"
    assert lc[-1].to_iso() == "2052-05-18"
    assert lp[1234].to_iso() == dates[1234].to_iso()
    sizes = {p: os.path.getsize(p) for p in ["dates.jsonl","dates.csv","dates.pkl"]}
    print("Sizes (bytes):", sizes)