import zipfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources"
OUT = ROOT / "build" / "usfm"

OUT.mkdir(parents=True, exist_ok=True)

for z in SRC.glob("*.zip"):
    target = OUT / z.stem
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z, "r") as zf:
        zf.extractall(target)
    print(f"Unpacked {z.name} -> {target}")


shutil.copy(
    "sources/25-JEReng-Prideaux.usfm",
    "build/usfm/eng-Prideaux_usfm"
)
