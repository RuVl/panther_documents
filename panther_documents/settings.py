"""
Django settings for panther_documents project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import django
# noinspection PyPackageRequirements
import environ
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

env = environ.Env(
    DEBUG=(bool, False)  # set casting, default value
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# noinspection SpellCheckingInspection
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# noinspection SpellCheckingInspection
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'currencies',
    'captcha.apps.CaptchaConfig',

    'authapp.apps.AuthConfig',
    'mainapp.apps.MainConfig',
    'paymentapp.apps.PaymentConfig'
]

if DEBUG:
    # Dummy caching (for development)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# TODO production cache

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'panther_documents.urls'

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
                'django.template.context_processors.request'
            ],
        },
    },
]

WSGI_APPLICATION = 'panther_documents.wsgi.application'

# Database
# noinspection SpellCheckingInspection
DATABASES = {
    'default': env.db()
}

# Password validation
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

# Custom login
AUTH_USER_MODEL = 'authapp.ShopUser'
LOGIN_URL = '/office/login/'

# Email config
EMAIL_CONFIG = env.email()

EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD']

EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']

DEFAULT_FROM_EMAIL = env.get_value('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

EMAIL_BACKEND = EMAIL_CONFIG['EMAIL_BACKEND']
EMAIL_USE_TLS = EMAIL_CONFIG.get('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = EMAIL_CONFIG.get('EMAIL_USE_SSL', False)

# Internationalization
USE_I18N = True
LANGUAGE_CODE = 'ru'
LOCALE_PATHS = (BASE_DIR / 'locale', )
LANGUAGES = (
    ('en-us', _('English')),
    ('ru', _('Russian')),
)


# Time settings
USE_TZ = True
TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'shared_static'
]  # Список нестандартных путей

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google reCAPTCHA
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

# Payments
PLISIO_SECRET_KEY = env('PLISIO_SECRET_KEY')

# Currency
SHOP_DEFAULT_CURRENCY = 'USD'
SHOP_CURRENCIES = ('USD', 'RUB')
OPENEXCHANGERATES_APP_ID = env('OPENEXCHANGERATES_APP_ID')

# Production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600  # Send browser auto redirect header
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
            }
        },
        'handlers': {
            'gunicorn': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'filename': BASE_DIR / 'logs' / 'django.log',
                'maxBytes': 1024 * 1024 * 100,  # 100 mb
            }
        },
        'loggers': {
            'gunicorn.errors': {
                'level': 'DEBUG',
                'handlers': ['gunicorn'],
                'propagate': True,
            },
        }
    }
