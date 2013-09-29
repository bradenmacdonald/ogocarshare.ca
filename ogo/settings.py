# Django settings for OGO

import os
import os.path

OGO_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(OGO_ROOT, os.path.pardir))

######################################################################
if 'DATABASE_URL' not in os.environ and 'DATABASE' not in os.environ:
    # Load the environment from .env
    # This lets us use ./manage.py without having to 'source .env' first
    ENV_FILE = PROJECT_ROOT + "/.env"
    with open(ENV_FILE) as f:
        envlines = f.readlines()
    for line in envlines:
        var, val = line.split('=', 1)
        val = val.strip()
        if val[0] == '"' and val[-1] == '"':
            val = val[1:-1]  # trim quotes
        os.environ[var] = val
# For PostgreSQL socket connections, we cannot use DATABASE_URL,
# so we set them up using DATABASE=dbname
if 'DATABASE_URL' in os.environ:
    # "e.g. postgres://user3123:passkja83kd8@ec2-117-21-174-214.compute-1.amazonaws.com:6212/db982398"
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
elif 'DATABASE' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DATABASE'],
            'HOST': '',
        }
    }
else:
    import sys
    sys.exit("No DB configured (!)")
######################################################################

DEBUG = (os.getenv("DEBUG", "no") == "yes")
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Braden MacDonald', 'webmaster@ogocarshare.ca'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['ogocarshare.ca', 'dev.ogocarshare.ca']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Vancouver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "user_media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(OGO_ROOT, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Whether Django should serve media files (user uploads) with its built-in server
SERVE_MEDIA_FILES = (os.getenv("SERVE_MEDIA_FILES", "yes" if DEBUG else "no") == "yes")

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('SECRET_KEY', None)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'ogo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ogo.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(OGO_ROOT, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'reversion',
    'easy_thumbnails',
    'mptt',
    'filer',
    'sekizai',
    'compressor',
    # CMS:
    'menus',
    'cms',
    'cms.plugins.text',
    # OGO:
    'ogo.plugins'
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

# Compressor settings:
COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OUTPUT_DIR = 'cache'  # lower-case the default "CACHE"
COMPRESS_PRECOMPILERS = (
    ("text/less", 'ogo.utils.compressor.LessFilter'),
)
COMPRESS_CSS_FILTERS = ['ogo.utils.compressor.CssAbsoluteFilterFixed']
if not DEBUG:
    COMPRESS_OFFLINE = True

# CMS Settings:
CMS_TEMPLATES = (
    ('ogo_cms_page.html', 'OGO Regular Page'),
)

# Filer settings:
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(PROJECT_ROOT, "site_media", "f"),
                'base_url': '/static/f/',
            },
            'UPLOAD_TO': 'ogo.utils.filer.filer_namer',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(PROJECT_ROOT, "site_media", "f_thumbs",),
                'base_url': '/static/f_thumbs/',
            },
        },
    },
}

# Car Share Everywhere API settings:
CSE_API_ENDPOINT = os.getenv('CSE_API_ENDPOINT', None)
