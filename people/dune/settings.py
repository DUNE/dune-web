# Django settings for dune project.

import os
import sys
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_BASE = os.path.dirname(PROJECT_PATH)

import socket
THIS_SERVER_NAME = socket.gethostname()


conf_file = os.path.join(PROJECT_BASE, 'people.conf')
assert os.path.exists(conf_file)
from ConfigParser import SafeConfigParser
conf = SafeConfigParser()
conf.read(conf_file)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Brett Viren', 'bv@bnl.gov'),

)

MANAGERS = ADMINS

DATABASES = {
    'default': dict(ENGINE = 'django.db.backends.sqlite3',
                    NAME = os.path.join(PROJECT_BASE, conf.get('database default', 'name')),
                    USER = conf.get('database default', 'name'),
                    PASSWORD = conf.get('database default', 'password'),
                    HOST = conf.get('database default', 'host'),
                    PORT = conf.get('database default', 'port')),
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_BASE, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/admin/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_BASE, "media"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = conf.get('common', 'secret_key', raw=True)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dune.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dune.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    os.path.join(PROJECT_PATH, 'templates'),
    '/usr/lib/python2.6/site-packages/django/contrib/admin/templates/admin',
)

# Must provide the expected default!
# https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'dune.context_processors.setting',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    #'django.contrib.admindocs',

    # for schema evolution:
    'south',

    'django_extensions',
    'members',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# a symbolic link to the pip site-packages
site_packages_dir = os.path.join(PROJECT_BASE,'site-packages')
assert os.path.exists(site_packages_dir)
if site_packages_dir not in sys.path:
    sys.path.insert(0, site_packages_dir)


print 'Running on server:', THIS_SERVER_NAME

if THIS_SERVER_NAME.startswith('dune'):
    DEBUG = TEMPLATE_DEBUG = True
    SITE_ROOT = '/web'
    DEFAULT_FROM_EMAIL = 'www@dune.bnl.gov'

elif THIS_SERVER_NAME.startswith('localhost'):
    DEBUG = TEMPLATE_DEBUG = True
    SITE_ROOT = '/web'
    DEFAULT_FROM_EMAIL = 'www@localhost'

elif THIS_SERVER_NAME.startswith('lycastus'):
    DEBUG = TEMPLATE_DEBUG = True
    SITE_ROOT = ''
    DEFAULT_FROM_EMAIL = 'www@localhost'

else:                           # ./manage.py runserver_plus
    DEBUG = TEMPLATE_DEBUG = True
    SITE_ROOT = ''
    DEFAULT_FROM_EMAIL = 'www@localhost'


VERSION='0.2.0'
DEFAULT_CHARSET = 'utf-8'
