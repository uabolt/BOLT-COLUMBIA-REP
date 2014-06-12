from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from interface import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="instructions.html"), name="instructions"),
    url(r'^pos/?$', views.pos_annotation, name='pos_annotation'),
    url(r'^reph/?$', views.reph_annotation, name='reph_annotation'),
    url(r'^finish/?$', TemplateView.as_view(template_name="finish.html"), name='finish'),
)

