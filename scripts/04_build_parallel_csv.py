import csv, json, re, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-b", action="store_true", help="Use the British English version of WEB")

args = parser.parse_args()


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data" / "mapping.csv"
if args.b:
    LXX = ROOT / "build" / "json" / "webbe_ESGV.json"
    MT  = ROOT / "build" / "json" / "webbe_EST.json"
    AT =  ROOT / "build" / "json" / "PrideauxBE_ESGA.json"
    OUT = ROOT / "build" / "esther_parallel_be.csv"
else:
    LXX = ROOT / "build" / "json" / "web_ESGV.json"
    MT  = ROOT / "build" / "json" / "web_EST.json"
    AT =  ROOT / "build" / "json" / "Prideaux_ESGA.json"
    OUT = ROOT / "build" / "esther_parallel.csv"

RANGE_RE = re.compile(r"^(\d+:\d+[a-z]?)\s*-\s*(\d+:\d+[a-z]?)$")

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
#    print(f"ch {ch}: v {v} suf {suf}")
    return ch, v, suf

def ref_sort_key(ref: str) -> tuple[int, int, int]:
    """
    Sort order: 40 < 40a < 40b < 41
    """
    ch, v, suf = parse_ref(ref)
    suf_ord = 0 if suf == "" else (ord(suf) - ord("a") + 1)
    return (ch, v, suf_ord)

def ref_to_tuple(ref: str):
    ch, v, suf = parse_ref(ref)
    suf_ord = 0 if suf == "" else (ord(suf) - ord("a") + 1)
    return (ch, v, suf_ord)

def expand_range_old(start: str, end: str):
#    print(f"start {start} - end {end}")
    sc, sv, ss = parse_ref(start)
    ec, ev, es = parse_ref(end)
    if ss or es:
        if sv != ev:
            raise ValueError(f"Ranges with suffixes not supported with different verse numbers: {start}-{end}")
        if ss == '':
                    return [f"{sc}:{sv}"]+[f"{sc}:{sv}{chr(ss)}" for ss in range(ord('a'), ord(es) + 1)]
#        print([f"{sc}:{sv}{chr(ss)}" for ss in range(ord(ss), ord(es) + 1)])
        return [f"{sc}:{sv}{chr(ss)}" for ss in range(ord(ss), ord(es) + 1)]
    if sc != ec:
        raise ValueError(f"Range crosses chapters: {start}-{end}")
    return [f"{sc}:{vv}" for vv in range(sv, ev + 1)]

def expand_ref_old(ref):
    if not ref.strip():
        return ["---"]
    m = RANGE_RE.match(ref.strip())
    if m:
#        print(f"RANGE_RE matched {ref} in expand_ref()")
        start, end = m.group(1), m.group(2)
        return expand_range(start, end)
    return [ref]
    
def get_text(dict, ref: str) -> str:
    if not ref.strip():
        return ""
    m = RANGE_RE.match(ref.strip())
    if m:
#        print(f"RANGE_RE matched {ref} in get_text()")
        start_ref, end_ref = m.group(1), m.group(2)
        keys = list(dict)
        start = keys.index(start_ref)
        end = keys.index(end_ref)
        parts = list(dict.values())[start:end+1]
        return " ".join(parts).strip()
#    print(f"no RANGE_RE match on {ref} in get_text()")
    return dict.get(ref.strip(), "")

def sort_key(ref: str):
    return ref_to_tuple(ref)

def row(rows, r, mt_dict, lxx_dict, at_dict):
    ch = r.get("ch")
    my_ref = r.get("my_ref")
    lxx_ref = r.get("lxx_ref")
    mt_ref  = r.get("mt_ref")
    at_ref  = r.get("at_ref")
    lxx_txt = get_text(lxx_dict,lxx_ref)
    mt_txt  = mt_dict.get(mt_ref,"")
    at_txt  = get_text(at_dict,at_ref)
    
#    print(f"ch=\"{ch}\" my_ref=\"{my_ref}\" mt_ref=\"{mt_ref}\" lxx_ref=\"{lxx_ref}\" at_ref=\"{at_ref}\"")
    if (not lxx_txt.strip()) and (not mt_txt.strip()) and (not at_txt.strip()): # don't add empty rows
        print(f"WARNING: Empty row at ch=\"{ch}\" my_ref=\"{my_ref}\" mt_ref=\"{mt_ref}\" lxx_ref=\"{lxx_ref}\" at_ref=\"{at_ref}\"")
        return rows
    rows.append({
        "ch": ch,
        "my_ref": my_ref,
        "mt_ref": mt_ref if mt_ref.strip() else "—",
        "mt_text": mt_txt,
        "lxx_ref": lxx_ref if lxx_ref.strip() else "—",
        "lxx_text": lxx_txt, 
        "at_ref": at_ref if at_ref.strip() else "—",
        "at_text": at_txt
        })
    return rows

def main():
    lxx_dict = json.loads(LXX.read_text(encoding="utf-8"))
    mt_dict  = json.loads(MT.read_text(encoding="utf-8"))
    at_dict  = json.loads(AT.read_text(encoding="utf-8"))

    rows = []
    with MAP.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows=row(rows, r, mt_dict, lxx_dict, at_dict)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ch","my_ref","mt_ref","mt_text","lxx_ref","lxx_text", "at_ref", "at_text"])
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {OUT} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
