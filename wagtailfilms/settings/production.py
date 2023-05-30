from .base import *

DEBUG = False
SECRET_KEY = "django-insecure-ktc2fm5ywc!5++^xz!*(ildzl7*lv7&f%io09^qcaf%!-z=_tz"
ALLOWED_HOSTS = ["*"]

try:
    from .local import *
except ImportError:
    pass
