import os
import sys      
sys.path.append('/var/www/w3/uabolt/chunker')
os.environ['DJANGO_SETTINGS_MODULE'] = 'chunker.production_settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
