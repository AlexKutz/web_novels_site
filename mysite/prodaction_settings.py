from pathlib import Path
import os.path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

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

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

COMPRESS_OFFLINE = True
