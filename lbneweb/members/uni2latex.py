#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Convert from unicode to LaTeX.
'''

import re
import os

def unicode_to_latex(tt = None, filename = None):
    '''Fill and return a translation table that converts from unicode
    to LaTeX symbols by parsing the utf8ienc.dtx file.
    Code is from: 
      http://stackoverflow.com/questions/4578912/
    The utf8ienc.dtx file can be had from:
      http://www.tex.ac.uk/CTAN/macros/latex/base/utf8ienc.dtx
    '''
    if not filename:
        mydir = os.path.dirname(__file__)
        filename = os.path.join(mydir, 'utf8ienc.dtx')

    tt = tt or dict()
    for line in open(filename):
        m = re.match(r'%.*\DeclareUnicodeCharacter\{(\w+)\}\{(.*)\}', line)
        if m:
            codepoint, latex = m.groups()
            latex = latex.replace('@tabacckludge', '') # remove useless (??) '@tabacckludge'
            tt[int(codepoint, 16)] = unicode(latex)
    return tt

def ascii_to_latex(tt = None):
    '''
    Do additional patch up
    '''
    tt = tt or dict()
    tt[ord('&')] = unicode(r'\&')
    tt[ord(u"í")] = unicode(r"\'{i}")
    return tt

def translation_table():
    tt = unicode_to_latex()
    tt = ascii_to_latex(tt)
    return tt

def test():
    data = [
        (u"été & à l'eau", r"\'et\'e \& \`a l'eau"),
        (u"Sérgio", r"S\'ergio"),
        (u"Poços", r"Po\c cos"),
        (u"Físicas", r"F\textasciiacute\isicas")
        ]
    for start, want in data:
        got = start.translate(translation_table())
        assert want == got, 'Failure "%s" != "%s"' % (want,got)
        print 'OK:',start,'-->',want,' =?= ',got


if '__main__' == __name__:
    test()

