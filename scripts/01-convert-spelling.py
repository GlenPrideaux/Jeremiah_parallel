#!/usr/bin/env python3
"""
Convert USFM files between American and British spelling.

Usage:
  python usfm_spelling_convert.py us2uk input.usfm output.usfm
  python usfm_spelling_convert.py uk2us input.usfm output.usfm
"""

import re
import sys
from pathlib import Path

US_TO_UK = {
    "honor": "honour",
    "Honor": "Honour",
    "color": "colour",
    "Color": "Colour",
    "favor": "favour",
    "Favor": "Favour",
    "labor": "labour",
    "Labor": "Labour",
    "rumor": "rumour",
    "Rumor": "Rumour",
    "center": "centre",
    "Center": "Centre",
    "theater": "theatre",
    "Theater": "Theatre",
    "defense": "defence",
    "Defense": "Defence",
    "offense": "offence",
    "Offense": "Offence",
    "traveler": "traveller",
    "Traveler": "Traveller",
    "traveled": "travelled",
    "Traveled": "Travelled",
    "traveling": "travelling",
    "Traveling": "Travelling",
    "counselor": "counsellor",
    "Counselor": "Counsellor",
    "counseling": "counselling",
    "Counseling": "Counselling",
    "gray": "grey",
    "Gray": "Grey",
}

UK_TO_US = {v: k for k, v in US_TO_UK.items()}

def convert_text(text: str, mapping: dict[str, str]) -> str:
    for src, dst in mapping.items():
        text = re.sub(rf"\b{re.escape(src)}\b", dst, text)
    return text

def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"us2uk", "uk2us"}:
        print(__doc__.strip())
        return 1

    mode, input_file, output_file = sys.argv[1:4]
    src = Path(input_file)
    dst = Path(output_file)

    text = src.read_text(encoding="utf-8")
    mapping = US_TO_UK if mode == "us2uk" else UK_TO_US
    text = convert_text(text, mapping)
    dst.write_text(text, encoding="utf-8")
    print(f"Wrote {dst}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
