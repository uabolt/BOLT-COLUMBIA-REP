from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
#from iraqiSpeakerVerifiers.views import Question1Create, Question1Update
from .views import *

urlpatterns = patterns('',
    url(r'answer1/add/$', MultipleChoiceVerificationCreate.as_view(), name='answer1_add'),
    url(r'sri/test/$', MultipleChoiceVerificationCreate.as_view(sri=True), name='sri-answer1_add'),
    #url(r'answer1/(?P<pk>\d+)/$', SpeakerVerificationUpdate.as_view(), name='answer1_update'),
    url(r'^iraqiSpeakerVerifiers/done/$', TemplateView.as_view(template_name='instructions.html'),
        name='verification_done'),
    url(r'^iraqiSpeakerVerifiers/success/$', test_passed, name='test_passed'),
    url(r'^iraqiSpeakerVerifiers/failure/$', test_failed, name='test_failed'),
    url(r'^sri/iraqiSpeakerVerifiers/success/$', test_passed, {'sri':True}, name='sri-test_passed'),
    url(r'^sri/iraqiSpeakerVerifiers/failure/$', test_failed, {'sri':True}, name='sri-test_failed'),
)
