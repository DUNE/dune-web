#!/usr/bin/env python
import os, sys
path = '/srv/www/django/duneweb'
if path not in sys.path:
    sys.path.append(path)
sys.path.append('/srv/www/venv/lib/python2.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dune.settings'

# mypython = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(mypython)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
def _application(environ, start_response):
    status = '200 OK'

    if not environ['mod_wsgi.process_group']:
      output = 'EMBEDDED MODE'
    else:
      output = 'DAEMON MODE'

    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
