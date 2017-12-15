all: BerichtV47.pdf

BerichtV47.pdf: BerichtV47.tex
	lualatex BerichtV47.tex

BerichtV47.tex: source/Theorie.tex

BerichtV47.tex: source/Auswertung.tex

source/Auswertung.tex: Berechnungen/plot_C_v.py
	python Berechnungen/plot_C_v.py
