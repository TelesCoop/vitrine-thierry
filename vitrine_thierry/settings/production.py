from .base import *  # noqa: F403 F401
import rollbar

DEBUG = False

SECRET_KEY = config.getstr("security.secret_key")  # noqa: F405
ALLOWED_HOSTS = config.getlist("security.allowed_hosts")  # noqa: F405
STATIC_ROOT = config.getstr("staticfiles.static_root")  # noqa: F405
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

WAGTAIL_ENABLE_UPDATE_CHECK = False  # Disable update alerts

WAGTAILADMIN_BASE_URL = "https://thierry-baudry.tlscp.fr"

# Mailgun
ANYMAIL = {
    "MAILGUN_API_KEY": config.getstr("mail.api_key"),  # noqa: F405
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
    "MAILGUN_SENDER_DOMAIN": "mail.telescoop.fr",
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@telescoop.fr"
SERVER_EMAIL = "no-reply@telescoop.fr"

# rollbar
MIDDLEWARE.append(  # noqa: F405
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware"
)

ROLLBAR = {
    "access_token": config.getstr("bugs.rollbar_access_token"),  # noqa: F405
    "environment": "production",
    "code_version": "1.0",
    "root": BASE_DIR,  # noqa: F405
}

rollbar.init(**ROLLBAR)

# BACKUP
INSTALLED_APPS.append("telescoop_backup")  # noqa: F405
BACKUP_ACCESS = config.getstr("backup.backup_access", None)  # noqa: F405
BACKUP_SECRET = config.getstr("backup.backup_secret", None)  # noqa: F405
BACKUP_BUCKET = config.getstr("backup.backup_bucket", None)  # noqa: F405
BACKUP_REGION = config.getstr("backup.backup_region", None)  # noqa: F405
