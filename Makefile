all: pdf

build/usfm/eng-Prideaux_usfm/25-JEReng-Prideaux.usfm: sources/25-JEReng-Prideaux.usfm
	mkdir -p build/usfm/eng-Prideaux_usfm/
	cp sources/25-JEReng-Prideaux.usfm build/usfm/eng-Prideaux_usfm/

WEB_USFM_ZIP := sources/eng-web_usfm.zip
WEBBE_USFM_ZIP := sources/eng-webbe_usfm.zip

ZIP_FILES := \
	$(WEB_USFM_ZIP) \
	$(WEBBE_USFM_ZIP) 

$(WEB_USFM_ZIP):
	mkdir -p build
	curl -L -o $@ https://ebible.org/Scriptures/eng-web_usfm.zip
$(WEB_USFM_ZIP):
	mkdir -p build
	curl -L -o $@ https://ebible.org/Scriptures/eng-webbe_usfm.zip

WEB_USFMS := \
	build/usfm/eng-web_usfm/25-JEReng-web.usfm \
	build/usfm/eng-web_usfm/25-JEReng-webbe.usfm

$(WEB_USFMS): scripts/01_unpack_sources.py $(ZIP_FILES)
	python3 scripts/01_unpack_sources.py

USFM_FILES := \
	build/usfm/eng-Prideaux_usfm/25-JEReng-Prideaux.usfm \
	build/usfm/eng-web_usfm/25-JEReng-web.usfm \
	build/usfm/eng-web_usfm/25-JEReng-webbe.usfm
unpack: USFM_FILES

JSON_FILES := \
	build/json/prideaux_JER.json \
	build/json/web_JER.json \
	build/json/webbe_JER.json
$(JSON_FILES): scripts/02_parse_usfm.py $(USFM_FILES)
	python3 scripts/02_parse_usfm.py

json: $(JSON_FILES)

CSV_FILES := build/jeremiah_parallel.csv build/jeremiah_parallel_be.csv

build/jeremiah_parallel.csv: build/json/prideaux_JER.json build/json/web_JER.json
	python3 scripts/04_build_parallel_csv.py

build/jeremiah_parallel_be.csv: build/json/prideaux_JER.json build/json/webbe_JER.json
	python3 scripts/04_build_parallel_csv.py -b

csv: $(CSV_FILES)

tex/jeremiah_parallel.tex: scripts/05_csv_to_tex.py build/jeremiah_parallel.csv
	python3 scripts/05_csv_to_tex.py

tex/jeremiah_parallel_be.tex: scripts/05_csv_to_tex.py build/jeremiah_parallel_be.csv
	python3 scripts/05_csv_to_tex.py -b

tex: tex/jeremiah_parallel.tex tex/jeremiah_parallel_be.tex 

TEX_FILES := \
	tex/jeremiah_parallel.tex \
	tex/intro.tex \
	tex/preamble.tex \
	tex/title.tex \
	tex/copyright.tex \
	tex/jeremiah_book.tex
tex/jeremiah_book.pdf: $(TEX_FILES)
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error jeremiah_book.tex

jeremiah_book.pdf: tex/jeremiah_book.pdf
	cp tex/jeremiah_book.pdf .

TEX_FILES_BE := \
	tex/jeremiah_parallel_be.tex \
	tex/intro_be.tex \
	tex/preamble.tex \
	tex/title_be.tex \
	tex/copyright_be.tex \
	tex/jeremiah_book_be.tex
tex/jeremiah_book_be.pdf: $(TEX_FILES_BE)
	cd tex && latexmk -xelatex -interaction=nonstopmode -halt-on-error jeremiah_book_be.tex

jeremiah_book_be.pdf: tex/jeremiah_book_be.pdf
	cp tex/jeremiah_book_be.pdf .

pdf: jeremiah_book.pdf jeremiah_book_be.pdf

.PHONY: unpack json csv tex pdf all clean
clean:
	rm -rf build/*
	rm -f tex/*.aux tex/*.log tex/*.out tex/*.pdf
	rm -f tex/jeremiah_book*.fls tex/jeremiah_book*.xdv tex/jeremiah_book*.fdb_latexmk
