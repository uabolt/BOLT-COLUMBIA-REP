from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import interface.urls
import iraqiSpeakerVerifiers.urls
import iraqiSpeakerVerifiers as verifier

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chunker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^/?$', verifier.views.SpeakerVerificationCreate.as_view(), name='root'),
    url(r'^/?$', verifier.views.ConsentVerificationCreate.as_view(), name='root'),
    url(r'^annotations/', include(interface.urls)),
    url(r'^verify/', include(iraqiSpeakerVerifiers.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
