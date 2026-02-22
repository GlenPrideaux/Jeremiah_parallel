import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "build" / "jeremiah_parallel.csv"
OUT = ROOT / "tex" / "jeremiah_parallel.tex"

FOOTNOTE_DELIM = "\u241EFOOTNOTE\u241E"

import re

HEBREW_RE = re.compile(r'[\u0590-\u05FF]+')

def wrap_hebrew(text):
    return HEBREW_RE.sub(lambda m: r'\texthebrew{' + m.group(0) + '}', text)

def inject_latex_footnotes(escaped_text: str) -> str:
    # escaped_text is already LaTeX-escaped
    parts = escaped_text.split(FOOTNOTE_DELIM)
    if len(parts) == 1:
        return escaped_text

    out = [parts[0]]
    # parts alternates: text, footnote, text, footnote, ...
    for i in range(1, len(parts), 2):
        fn = parts[i].strip()
        if fn:
            out.append(r"\footnote{" + fn + "}")
        if i + 1 < len(parts):
            out.append(parts[i + 1])
    return "".join(out)

def esc(s: str) -> str:
    if s is None:
        return ""
    s = s.replace("\\", r"\textbackslash{}")
    s = s.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$")
    s = s.replace("#", r"\#").replace("_", r"\_").replace("{", r"\{").replace("}", r"\}")
    s = s.replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")
    return s

STRUCT_DELIM = "\u241E"

def render_structured_to_latex(escaped_text: str) -> str:
    # escaped_text already LaTeX-escaped and Hebrew-wrapped if you do that step.
    if STRUCT_DELIM not in escaped_text:
        return escaped_text

    parts = escaped_text.split(STRUCT_DELIM)
    out = []
    i = 0
    while i < len(parts):
        token = parts[i]
        if token.startswith("Q:"):
            indent = int(token[2:]) if token[2:].isdigit() else 1
            if i + 1 < len(parts):
                line = parts[i + 1].strip()
                out.append(rf"\poemline{{{indent}}}{{{line}}}")
                i += 2
            else:
                i += 1
        elif token == "P":
            if i + 1 < len(parts):
                out.append(parts[i + 1].strip() + " ")
                i += 2
            else:
                i += 1
        else:
            # plain text (fallback)
            if token.strip():
                out.append(token.strip() + " ")
            i += 1

    rendered = "".join(out).strip()

    # If any poemlines were used, wrap in a group that keeps \\ safe
    if r"\poemline" in rendered:
        rendered = r"{\raggedright " + rendered + "}"
    return rendered

def parse_ref(ref: str) -> tuple[int, int]:
    # ref like "12:7" (ignore any suffixes if you later add them)
    ch_s, v_s = ref.split(":", 1)
    # if you ever use 7a/7* etc, keep only leading digits for verse
    v_digits = "".join(c for c in v_s if c.isdigit())
    return int(ch_s), int(v_digits) if v_digits else 0

def main():
    rows = []
    with INP.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as out:
        out.write(r"""\input{preamble.tex}
\begin{document}
\input{intro}
\section*{Jeremiah (Parallel) — LXX order}
""")

        current_ch = None
        for r in rows:
            ch, _ = parse_ref(r["lxx_ref"])
            if ch != current_ch:
                if current_ch is not None:
                    out.write("\\end{paracol}\n")
                out.write(f"\\ChapterHeading{{{ch}}}\n")
                out.write("\\begin{paracol}{2}\n")
                current_ch = ch

            lxx_ref = esc(r["lxx_ref"])
            mt_ref  = esc(r["mt_ref"])
            lxx_txt = render_structured_to_latex(inject_latex_footnotes(wrap_hebrew(esc(r["lxx_text"]))))
            mt_txt  = render_structured_to_latex(inject_latex_footnotes(wrap_hebrew(esc(r["mt_text"]))))
            out.write(f"\\VersePair{{{lxx_ref}}}{{{lxx_txt}}}{{{mt_ref}}}{{{mt_txt}}}\n")

        out.write(r"""\end{paracol}
\end{document}
""")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
