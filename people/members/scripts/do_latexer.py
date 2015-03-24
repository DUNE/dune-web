#!/usr/bin/env python
from members import latexer
def run(argv):
    template = argv
    print latexer.process_latex(template)




