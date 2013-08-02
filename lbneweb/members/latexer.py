#!/usr/bin/env python
'''
http://djangosnippets.org/snippets/102/
'''

from subprocess import call, check_call, PIPE
from os import remove, rename, getcwd, chdir
from os.path import dirname, exists
from tempfile import mkdtemp
from shutil import rmtree
from django.template import loader, Context

from contextlib import contextmanager

@contextmanager
def tempdir(cd = False, delete=True):
    td = mkdtemp()
    olddir = None
    if cd:
        olddir = getcwd()
        chdir(td)
    yield td
    if olddir:
        chdir(olddir)
    if delete:
        rmtree(td)
    
def process_latex(template, context={}, type='pdf', outfile=None):
    """
    Processes a template as a LaTeX source file.
    Output is either being returned or stored in outfile.
    At the moment only pdf output is supported.
    """

    t = loader.get_template(template)
    c = Context(context)
    r = t.render(c)

    name = 'doc'
    exts = "tex log aux pdf dvi png".split()
    names = dict((x, '%s.%s' % (name, x)) for x in exts)
    infn = names['tex']
    outfn = names[type]

    with tempdir(cd=True, delete = False) as td:
        print 'Tempdir:',td
        with open(infn,'w') as tex:
            tex.write(r)

        call(['pdflatex', '-interaction=nonstopmode', '-output-format', type, name],
             stdout=PIPE, stderr=PIPE)
        call(['pdflatex', '-interaction=nonstopmode', '-output-format', type, name],
             stdout=PIPE, stderr=PIPE)
        if not exists(outfn):
            print open('doc.log').read()
        out = open(outfn).read()
    return out
    
