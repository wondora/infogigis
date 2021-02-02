from .base import *
import os, environ

def read_secret(secret_name):
    with open('/run/secrets' + secret_name) as f:
        secret = f.read()
        secret = secret.strip()
    return secret 

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = read_secret('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'infogigi',
        'USER':'wondora',
        'PASSWORD':read_secret('MYSQL_PASSWORD'),
        'HOST':'mariadb',
        'PORT':'3306',
    }
}