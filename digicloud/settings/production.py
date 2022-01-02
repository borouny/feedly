from digicloud.settings.base import *  # noqa F403v

DEBUG = True # noqa F405

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # noqa F405
        'NAME': config('DATABASE_NAME', default='postgres'),  # noqa F405
        'USER': config('DATABASE_USER', default='postgres'),  # noqa F405
        'PASSWORD': config('DATABASE_PASSWORD', default='postgres'),  # noqa F405
        'HOST': config('DATABASE_HOST', default='localhost'),  # noqa F405
        'PORT': config('DATABASE_PORT', default='5432'),  # noqa F405
    }
}
