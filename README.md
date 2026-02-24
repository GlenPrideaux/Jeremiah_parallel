# Jeremiah Parallel Edition
This project generates the parallel English edition of Jeremiah based on Septuagint verse order.

The output file is found in the tex subfolder.

To compile this from sources you will need to install the following fonts: [TeX Gyre Pagella](https://ctan.org/pkg/tex-gyre-pagella?lang=en) and [Ezra SIL](https://software.sil.org/ezra/).

- To unpack the sources:
  - `make unpack`

- To build the json sources:
  - `make json`

- To combine the json sources into a CSV file, one record per verse:
  - `make csv`

- To create the LaTeX source:
  - `make tex`

- To rebuild the PDF:
  - `make pdf` or `make all` or simply `make`

- To delete logs and intermediate files and output pdf:
  - `make clean`
