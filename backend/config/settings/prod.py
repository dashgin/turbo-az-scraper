import os

from .base import * # noqa
import dj_database_url
import django_heroku


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ADMIN_URL = os.environ.get('ADMIN_URL')

django_heroku.settings(locals())
