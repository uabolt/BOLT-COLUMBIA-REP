from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.conf import settings
from interface import views

urlpatterns = patterns('',
    url(r'^$', views.instructions, name="instructions"),
    url(r'^pos/?$', views.pos_annotation, name='pos_annotation'),
    url(r'^reph/?$', views.reph_annotation, name='reph_annotation'),
    #url(r'^finish/?$', TemplateView.as_view(template_name="finish.html"), name='finish'),
    url(r'^finish/?$', views.finish, name='finish'),
)
