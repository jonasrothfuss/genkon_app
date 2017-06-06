from .settings_conf.development import *

with open('./secret_key.txt') as f:
  SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']