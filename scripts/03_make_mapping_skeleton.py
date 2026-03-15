import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BR_JSON = ROOT / "build" / "json" / "brenton_JER.json"
OUT = ROOT / "data" / "mapping_lxx_to_mt.csv"

import re

REF_RE = re.compile(r'^(\d+):(\d+)([a-z]?)$', re.IGNORECASE)

def parse_ref(ref: str) -> tuple[int, int, str]:
    """
    Parses '24:40a' -> (24, 40, 'a')
           '24:40'  -> (24, 40, '')
    """
    ref = ref.strip()
    m = REF_RE.match(ref)
    if not m:
        raise ValueError(f"Bad ref format: {ref!r}")
    ch = int(m.group(1))
    v  = int(m.group(2))
    suf = (m.group(3) or "").lower()
    return ch, v, suf

def ref_sort_key(ref: str) -> tuple[int, int, int]:
    """
    Sort order: 40 < 40a < 40b < 41
    """
    ch, v, suf = parse_ref(ref)
    suf_ord = 0 if suf == "" else (ord(suf) - ord("a") + 1)
    return (ch, v, suf_ord)

def sort_key(ref: str):
    return ref_sort_key(ref)

def main():
    verses = json.loads(BR_JSON.read_text(encoding="utf-8"))
    refs = sorted(verses.keys(), key=sort_key)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lxx_ref", "mt_ref"])
        for r in refs:
            w.writerow([r, r])  # identity placeholder
    print(f"Wrote skeleton mapping with {len(refs)} rows -> {OUT}")

if __name__ == "__main__":
    main()
