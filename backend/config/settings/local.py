from .base import * # noqa

SECRET_KEY = 'django-insecure-secret-key'

DEBUG = True

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
