from .base import *


env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}