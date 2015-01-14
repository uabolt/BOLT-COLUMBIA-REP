from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
#from iraqiSpeakerVerifiers.views import Question1Create, Question1Update
from iraqiSpeakerVerifiers.views import SpeakerVerificationCreate, SpeakerVerificationUpdate

urlpatterns = patterns('',
    url(r'answer1/add/$', SpeakerVerificationCreate.as_view(), name='answer1_add'),
    url(r'answer1/(?P<pk>\d+)/$', SpeakerVerificationUpdate.as_view(), name='answer1_update'),
    url(r'^done/$', TemplateView.as_view(template_name='instructions.html'),
        name='verification_done'),
)
