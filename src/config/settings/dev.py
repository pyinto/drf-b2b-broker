from .base import *  # noqa: F403


DEBUG = True


INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]

ALLOWED_HOSTS += [  # noqa: F405
    *INTERNAL_IPS,
]


# Dev-Specific Apps:
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_extensions",
]

# Dev-Specific Middlewares:
MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
