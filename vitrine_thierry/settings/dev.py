from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-v+=mi0xmtt9&48d(hpfeidam$bxe)yoap*fj$qu*gz2&3@j*m)"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"

try:
    from .local import *
except ImportError:
    pass
