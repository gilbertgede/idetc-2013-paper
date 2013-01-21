# type "make" command in Unix to create asme2e.pdf file
all:
	latex asme2e.tex
	bibtex asme2e.aux
	latex asme2e.tex
	latex asme2e.tex
	dvipdf asme2e.dvi asme2e.pdf

clean:
	(rm -rf *.ps *.log *.dvi *.aux *.*% *.lof *.lop *.lot *.toc *.idx *.ilg *.ind *.bbl *blg)
