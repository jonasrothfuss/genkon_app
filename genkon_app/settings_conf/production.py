from .base import *
import os

#with open(os.path.join(BASE_DIR,'genkon_app/secret_key.txt')) as f:
#  SECRET_KEY = f.read().strip()

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

#with open(os.path.join(BASE_DIR,'genkon_app/db_password.txt')) as f:
#  DB_PASSWORD = f.read().strip()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'WARNING',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['db_log'],
            'level': 'WARNING',
            'propagate': True,
        }
    }
}

aws_secret_key_file = os.path.join(BASE_DIR,'genkon_app/aws_secret_key.txt')
if os.path.isfile(aws_secret_key_file) :
    with open(aws_secret_key_file) as f:
        aws_secret_key = f.read().strip()
else:
    aws_secret_key = None


# AWS S3 Filestorage
#os.environ['S3_USE_SIGV4'] = 'True'
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAIQIHU3PO3JX44HJQ')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', aws_secret_key)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'genkon-app-storage')
S3_USE_SIGV4 = True
AWS_QUERYSTRING_AUTH = False

AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_CLOUDFRONT_DOMAIN', 'd23ftheat9c160.cloudfront.net')

MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN +'/%s/' % MEDIAFILES_LOCATION


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)