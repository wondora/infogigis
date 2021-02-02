from .base import *
import os, environ


env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = "0lb#yu$t1r8_+0g-yt33@y)ge2(&+4_$r84&hi(7#tz3l^yo21"
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'infogigi',
        'USER':'wondora',
        'PASSWORD':'MYSQL_PASSWORD',
        'HOST':'mariadb',
        'PORT':'3306',
    }
}