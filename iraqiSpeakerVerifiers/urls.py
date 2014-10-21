from django.conf.urls import patterns, url
from iraqiSpeakerVerifiers.views import Question1Create, Question1Update

urlpatterns = patterns('',
    url(r'answer1/add/$', Question1Create.as_view(), name='answer1_add'),
    url(r'answer1/(?P<pk>\d+)/$', Question1Update.as_view(), name='answer1_update'),
    url(r'^done/$', TemplateView.as_view(template_name='imagetask/done.html'),
        name='answer1_done'),
)

