import os
from chunker.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost', 'b4.sista.arizona.edu']


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    },

    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'uabolt',
        'USER': 'enoriega',
        'PASSWORD': 'w7PxNoAojIWsDA',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = 'http://w3.sista.arizona.edu/mt_uabolt/static/'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ar-iq'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Dataset files directory
DATASET_DIR = "%s/../dataset/" % BASE_DIR
