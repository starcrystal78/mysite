from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dqe66usnbic!^*3_#inopmq3jf-t4yd8s=@h#pnqawmst-++p@'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

MIDDLEWARE = MIDDLEWARE + [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
CACHES ={
    "default":{
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "D:\Projects\Django-test\wagtail -Test\Cache"
    }

}

try:
    from .local import *
except ImportError:
    pass
