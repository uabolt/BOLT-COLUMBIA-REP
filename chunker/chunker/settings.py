"""
Django settings for chunker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i+ezy@8tw9^vu=#13is-%2wsak*k7@)@rv5529l4uxuhi4#hqt'




# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'interface',
    'iraqiSpeakerVerifiers',
    'bootstrap_toolkit_bolt',
    'catalogs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'interface.middleware.dataset.VerifyTestTaken',
    'interface.middleware.dataset.AssignDataset',
    'interface.middleware.language.AdminLocaleURLMiddleware',
)

ROOT_URLCONF = 'chunker.urls'

WSGI_APPLICATION = 'chunker.wsgi.application'

STATIC_ROOT='static/'


# Locale directories paths
LOCALE_PATHS = ( "%s/locale/" % BASE_DIR,)

ADMIN_LANGUAGE_CODE = "en_US"

SESSION_SAVE_EVERY_REQUEST = True

FIXTURE_DIRS = ( '%s/fixtures/' % BASE_DIR,)

MAX_ANNOTATIONS = 3 # Max number of annotations per item
TASK_SIZE = 10 # Number of annotations that complete a task
