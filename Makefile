all: pdf

build/usfm/eng-Prideaux_usfm/25-JEReng-Prideaux.usfm: sources/25-JEReng-Prideaux.usfm
	mkdir -p build/usfm/eng-Prideaux_usfm/
	cp sources/25-JEReng-Prideaux.usfm build/usfm/eng-Prideaux_usfm/

build/usfm/eng-web_usfm/25-JEReng-web.usfm: scripts/01_unpack_sources.py sources/eng-web_usfm.zip
	python3 scripts/01_unpack_sources.py

unpack: build/usfm/eng-Prideaux_usfm/25-JEReng-Prideaux.usfm build/usfm/eng-web_usfm/25-JEReng-web.usfm

build/json/prideaux_JER.json: scripts/02_parse_usfm.py build/usfm/eng-Prideaux_usfm/25-JEReng-Prideaux.usfm
	python3 scripts/02_parse_usfm.py

build/json/web_JER.json: scripts/02_parse_usfm.py build/usfm/eng-web_usfm/25-JEReng-web.usfm
	python3 scripts/02_parse_usfm.py

json: build/json/prideaux_JER.json build/json/web_JER.json

build/jeremiah_parallel.csv: build/json/prideaux_JER.json build/json/web_JER.json
	python3 scripts/04_build_parallel_csv.py

csv: build/jeremiah_parallel.csv

tex/jeremiah_parallel.tex: scripts/05_csv_to_tex.py build/jeremiah_parallel.csv
	python3 scripts/05_csv_to_tex.py

tex: tex/jeremiah_parallel.tex

tex/jeremiah_book.pdf: tex/jeremiah_parallel.tex tex/intro.tex tex/preamble.tex tex/title.tex tex/copyright.tex tex/jeremiah_book.tex
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error jeremiah_book.tex

jeremiah_book.pdf: tex/jeremiah_book.pdf
	cp tex/jeremiah_book.pdf .

pdf: jeremiah_book.pdf 

.PHONY: clean
clean:
	rm -rf build/*
	rm -f tex/*.aux tex/*.log tex/*.out tex/*.pdf
	rm -f tex/jeremiah_book.fls tex/jeremiah_book.xdv tex/jeremiah_book.fdb_latexmk
