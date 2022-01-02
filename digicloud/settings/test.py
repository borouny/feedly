from digicloud.settings.base import *  # noqa F403

DEBUG = True  # noqa F405

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa F405
    }
}
