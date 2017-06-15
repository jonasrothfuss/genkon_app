from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '05)y=!cu*o(8b)y+#lri+(rydh4j%cesnhh%#@wj^xoz=pu_4='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}