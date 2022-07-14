from pathlib import Path
import os.path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insec2312$#$@#$^ad213urej9t-xcll4x)ghqk9fa4_muse=ncqaxa'

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'user',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'POST': '5432'
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static_collected')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

COMPRESS_OFFLINE = True