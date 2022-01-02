from pathlib import Path
import sys
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ci5n!4iq6(m*6m_yq4*f3u2j7ku-7%33#pmi=dba_34!7d10p)'
DEBUG = True
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
AUTHENTICATION_BACKENDS = ('digicloud.user_management.servieces.authentication.EmailModelBackend',)

ALLOWED_HOSTS = []
HOST_BASE_URL = config("HOST_BASE_URL", 'http://127.0.0.1:8000')
CORS_ORIGIN_ALLOW_ALL = False
cors_whitelist_domains = list(set(
    ALLOWED_HOSTS + ['127.0.0.1', 'localhost'] + config('CORS_WHITELIST', default=[])
))

CORS_ORIGIN_WHITELIST = (cors_whitelist_domains +
                         ['https://' + item for item in cors_whitelist_domains] +
                         ['http://' + item for item in cors_whitelist_domains]
                         )

CORS_ALLOW_METHODS = (
    'GET',
    'PUT',
    'POST',
    'DELETE',
    'PATCH'
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'knox',
    'digicloud.user_management',
    'digicloud.feed_management',
    'digicloud.fetcher',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'user_management.User'

ROOT_URLCONF = 'digicloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'digicloud.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'
    ),
    'PAGE_SIZE': 10
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': F"{BASE_DIR}/log.log",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'celery': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'test_yektanet': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },

    },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

RABBIT_HOST = config("RABBIT_HOST", default='localhost')

CELERY_BROKER_URL = config('CELERY_BROKER', 'amqp://{}'.format(RABBIT_HOST))
CELERY_TIMEZONE = TIME_ZONE
