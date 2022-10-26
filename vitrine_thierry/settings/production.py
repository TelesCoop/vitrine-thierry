from .base import *  # noqa: F403 F401

DEBUG = True

SECRET_KEY = config.getstr("security.secret_key")  # noqa: F405
ALLOWED_HOSTS = config.getlist("security.allowed_hosts")  # noqa: F405
STATIC_ROOT = config.getstr("staticfiles.static_root")  # noqa: F405
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

WAGTAIL_ENABLE_UPDATE_CHECK = False  # Disable update alerts

WAGTAILADMIN_BASE_URL = "https://thierry-baudry.tlscp.fr"

ANYMAIL = {
    "MAILGUN_API_KEY": config.getstr("mail.api_key"),  # noqa: F405
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    "MAILGUN_SENDER_DOMAIN": "mail.telescoop.fr",
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@telescoop.fr"
SERVER_EMAIL = "no-reply@telescoop.fr"
