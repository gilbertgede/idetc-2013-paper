pdf:
	latex asme2e.tex
	bibtex asme2e.aux
	latex asme2e.tex
	latex asme2e.tex
	dvipdf asme2e.dvi

clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *blg)
