all: BerichtV47.pdf

BerichtV47.pdf: BerichtV47.tex
	lualatex BerichtV47.tex

BerichtV47.tex: source/Theorie.tex

BerichtV47.tex: source/Auswertung.tex

source/Auswertung.tex: Berechnungen/plot_C_v.py Tabellen/Widerstand1.tex Tabellen/C_V_und_C_P.tex
	lualatex BerichtV47.tex

Berechnungen/plot_C_v.py: Daten/widerstand1.txt
	pyhton Berechnungen/plot_C_v.py
