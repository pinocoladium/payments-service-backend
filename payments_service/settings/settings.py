import os

from payments_service.settings.env_reader import env


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.str('DEBUG')

SERVER_HOST = env.str('SERVER_HOST')

ALLOWED_HOSTS = [
    SERVER_HOST,
]

INSTALLED_APPS = [
    # Extensions
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_celery_beat',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'rest_framework.authtoken',
    # Project applications
    'apps.payment_applications.apps.PaymentApplicationsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'payments_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'payments_service.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DEFAULT_DB_HOST'),
        'PORT': env('DEFAULT_DB_PORT'),
    },
}

# Celery
CELERY_BROKER_URL = env.str('CACHE_URL')

APP_CELERY = 'payments_services.celery.app'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'
CELERY_ALWAYS_EAGER = False
CELERY_BEAT_SCHEDULE = {
    'archive_payment_applications': {
        'task': 'apps.payment_applications.tasks.archive_payment_applications',
        'schedule': 60,  # каждую минуту
    },
}

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


TIME_ZONE = 'Asia/Yekaterinburg'
USE_TZ = True

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'ru'
LANGUAGES = (('ru', 'Русский'),)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/ev_api/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
