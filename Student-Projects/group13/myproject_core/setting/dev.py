# Development settings
from myproject_core.settings import *

SECRET_KEY = 'django-insecure-*$nhl)084p!_v)l19r6lngjlhs_6*7la!o&4g&5_ey93b+7upt'
HUGGINGFACE_API_KEY = 'api-key'
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
