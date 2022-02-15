# type: ignore
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9cbp7(tlf#(ytlwt^4xz!vr$o6(3_12y&+1ek%bw)0zjeo2b!x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# USER CUSTOM USER
AUTH_USER_MODEL = "people.User"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "softeng",
        "USER": "softeng",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
