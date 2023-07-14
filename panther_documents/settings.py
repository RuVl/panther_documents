"""
Django settings for panther_documents project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

# noinspection PyPackageRequirements
import environ
from pathlib import Path
# from django.utils.translation import gettext_lazy as _

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

ALLOWED_HOSTS = [
    '127.0.0.1',
    # '192.168.0.142'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mainapp.apps.MainConfig',
    'authapp.apps.AuthappConfig'
]

# Dummy caching (for development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'panther_documents.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
# LOGIN_URL = '/login/'

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
# LANGUAGES = (
#     ('en-us', _('English')),
#     ('ru', _('Russian')),
# )

# Time settings
USE_TZ = True
TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / STATIC_URL
STATICFILES_DIRS = []  # Список нестандартных путей

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
