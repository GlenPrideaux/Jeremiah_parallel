# Jeremiah Parallel Edition
### An English Alignment of the Septuagint and Masoretic Text Traditions

[![DOI](https://zenodo.org/badge/1163681430.svg)](https://doi.org/10.5281/zenodo.18811593)

---

## Overview

This project presents a verse-aligned English parallel edition of the Book of Jeremiah in its two principal textual traditions:

- The **Masoretic Text (MT)**
- The **Greek Septuagint (LXX)**

The Septuagint version of Jeremiah is significantly shorter and differently arranged than the Masoretic Text. These differences reflect distinct literary editions preserved in antiquity rather than simple translational variation.

This edition aligns the two traditions verse-by-verse in English translation using the Septuagint order as the structural framework. Where material is absent from one tradition, this is explicitly indicated.

The purpose of this work is to make structural and literary differences between the two textual traditions accessible to readers without requiring knowledge of Hebrew or Greek.

---

## Publication

The stable, citable edition is available via Zenodo:

> Prideaux, Glen. *Jeremiah Parallel Edition: An English Alignment of the Septuagint and Masoretic Text Traditions.* Zenodo, 2026.  
> https://doi.org/10.5281/zenodo.18811099

This repository contains the source files and build system used to generate the published edition.

---

## Textual Sources

Masoretic tradition represented through:

- **World English Bible (WEB)**  
  USFM digital distribution via eBible.org

Septuagint tradition represented through:

- **L. C. L. Brenton**, *The Septuagint Version of the Old Testament* (1851)  
  USFM digital distribution via eBible.org

Original USFM source files obtained from:
https://ebible.org

This edition does not constitute a new translation but a structured comparative presentation.

---

## Methodology

- Alignment is performed at the verse level.
- Septuagint ordering is used as the primary structural framework.
- Material absent from one tradition is explicitly marked.
- No attempt is made to harmonise or reconstruct a hypothetical original text.
- The edition is documentary and comparative in purpose.

The work is intended as a research and teaching tool in:

- Textual criticism
- Septuagint studies
- Hebrew Bible literary history
- Prophetic book formation
- Digital humanities

---

## Repository Structure
```
sources/      → Original USFM source files
data/         → Mapping table, LXX and MT verse by verse
build/        → Generated files
scripts/      → Parsing and conversion scripts
tex/          → LaTeX sources
```
---

## Building the Edition

Requirements:

- Python 3.x
- XeLaTeX
- Make

To build:
```
make
```

---

## Citation

If you use this edition, please cite the Zenodo publication:

> Prideaux, Glen. *Jeremiah Parallel Edition: An English Alignment of the Septuagint and Masoretic Text Traditions.* Zenodo, 2026. https://doi.org/10.5281/zenodo.18811099

---

## License

This project is licensed under:

Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)

You are free to share and adapt the work for non-commercial purposes with attribution.

---

## Contact

Feedback, corrections, and scholarly comments are welcome via GitHub
Issues.

