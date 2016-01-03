from django.conf.urls import url
from .views import api, core, search

urlpatterns = [

    url(r'^/?$', core.index),
    url(r'^ack/?$', api.ack),

    url(r'^search/?$', search.search, name="search"),
]
