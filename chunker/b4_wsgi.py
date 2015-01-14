import os
import sys      
sys.path.insert(0, '/var/www/virtualenvs/UA-BOLT/lib/python2.7/site-packages')
sys.path.append('/var/www/uabolt/chunker')
os.environ['DJANGO_SETTINGS_MODULE'] = 'chunker.b4_settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
