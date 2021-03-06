"""
Django settings for kegstarter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'et$8@u2fmznax!-_hx$1@y4x5u9$!w-4d2l@9+e)fbl@mt8he&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'south', # Schema migrations
    'mptt', # Commenting
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'main.context_processors.user_stats.get_user_votes',
    'main.context_processors.logo_hint.get_hints',
)

ROOT_URLCONF = 'kegstarter.urls'

WSGI_APPLICATION = 'kegstarter.wsgi.application'

LOGIN_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Untappd API keys (override in local_settings.py)
UNTAPPD_CLIENT_ID = ''
UNTAPPD_CLIENT_SECRET = ''
UNTAPPD_REDIRECT_URL = ''
UNTAPPD_COOKIE = 'untappd_token'

# Import overrides from local_settings.py
# DO NOT ADD ANYTHING BELOW THIS!
try:
    from local_settings import *
except:
    pass
