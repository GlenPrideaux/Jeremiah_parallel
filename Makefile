all: tex pdf

unpack:
	python3 scripts/01_unpack_sources.py

json: unpack
	python3 scripts/02_parse_usfm.py

mapping: json
	python3 scripts/03_make_mapping_skeleton.py

csv: json
	python3 scripts/04_build_parallel_csv.py

tex: csv
	python3 scripts/05_csv_to_tex.py

pdf: tex
	cd tex && xelatex -interaction=nonstopmode jeremiah_parallel.tex
	cp tex/jeremiah_parallel.pdf .

clean:
	rm -rf build/*
	rm -f tex/*.aux tex/*.log tex/*.out tex/*.pdf
