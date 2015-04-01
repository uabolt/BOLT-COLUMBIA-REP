from django.conf.urls import patterns, url
from django.conf import settings
from .views import *

urlpatterns = patterns('',
    url(r'^hits/?$', HITListView.as_view(), name="hit-list"),
    url(r'^([a-fA-F0-9]{32})/pos/?$', POSListView.as_view(), name="hit-pos-list"),
    url(r'^([a-fA-F0-9]{32})/reph/?$', RephListView.as_view(), name="hit-reph-list"),
    url(r'^pos/(?P<pk>\d+)/?$', POSDetailView.as_view(), name="hit-pos-detail"),
    url(r'^reph/(?P<pk>\d+)/\n+/?$', RephDetailView.as_view(), name="hit-reph-detail"),
)
