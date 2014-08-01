from django.contrib import admin
from interface.models import POSAnnotation, RephAnnotation, POSTag

# Register your models here.
admin.site.register(POSAnnotation)
admin.site.register(POSTag)
admin.site.register(RephAnnotation)
