from myproject_core.settings import *
import os


# Use environment variables in production
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

# Disable debug
DEBUG = False

# Specify your production domains
ALLOWED_HOSTS = ["example.com", "www.example.com"]

# -------------------------
# STATIC & MEDIA
# -------------------------
STATIC_ROOT = BASE_DIR / "staticfiles"  # for collectstatic
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# -------------------------
# DATABASE (PostgreSQL)
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB", "myproject_db"),
        'USER': os.environ.get("POSTGRES_USER", "myproject_user"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", "change_me"),
        'HOST': os.environ.get("POSTGRES_HOST", "localhost"),
        'PORT': os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# -------------------------
# SECURE COOKIES & SSL
# -------------------------
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


