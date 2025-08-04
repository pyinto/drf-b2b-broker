from .base import *  # noqa: F403


DEBUG = True

# Use weaker password hashing for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
