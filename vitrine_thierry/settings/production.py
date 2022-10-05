from .base import *  # noqa: F403 F401

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False  # Disable update alerts

try:
    from .local import *  # noqa: F403  F401
except ImportError:
    pass
