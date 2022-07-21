from pathlib import Path
import os.path

BASE_DIR = Path(__file__).resolve().parent.parent

with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = True 
DEBUG_PROPAGATE_EXCEPTIONS = False 

ALLOWED_HOSTS = ["212.8.246.107", "webnowellib.site"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'novel',
        'USER': 'alexandr',
        'PASSWORD': '9thl4duck',
        'HOST': 'localhost',
        'POST': ''
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = '/static_collected/'
STATICFILES_DIRS = [
            os.path.join(BASE_DIR, "novel", "static"),
                os.path.join(BASE_DIR, "static"),
                    os.path.join(BASE_DIR, "reader", "static"),
                        os.path.join(BASE_DIR, "authentication", "static")
                        ]

COMPRESS_OFFLINE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

CSRF_TRUSTED_ORIGINS = ['https://*.webnowellib.site','https://*.127.0.0.1']
