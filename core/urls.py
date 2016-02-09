from django.conf.urls import url
from .views import api, core, search, resolve, webhooks

urlpatterns = [

    url(r'^$', core.index),
    url(r'^ack/?$', api.ack),

    url(r'^search/?$', search.search, name="search"),

    # lookups based on the target URL, which is base64'd
    url(r'lookup/(?P<url_id>[a-zA-Z0-9\-]+)/?$', resolve.details, name="lookup-details"),
    url(r'lookup/(?P<url>[a-zA-Z0-9\-\_\=]+)/new$', resolve.start, name="lookup-start"),

    # Webhooks
    url(r'^webhook/dns/(?P<uuid>[a-zA-Z0-9\-]+)/ready/?$', webhooks.dns, name="webhook-dns"),
    url(r'^webhook/cacheddns/(?P<uuid>[a-zA-Z0-9\-]+)/ready/?$', webhooks.cachedDns, name="webhook-cacheddns"),
    url(r'^webhook/googledns/(?P<uuid>[a-zA-Z0-9\-]+)/ready/?$', webhooks.googleDns, name="webhook-googledns"),
    url(r'^webhook/opennicdns/(?P<uuid>[a-zA-Z0-9\-]+)/ready/?$', webhooks.openNicDns, name="webhook-opennicdns"),
    url(r'^webhook/asn/(?P<uuid>[a-zA-Z0-9\-]+)/ready/?$', webhooks.asn, name="webhook-asn"),
    url(r'^webhook/whois/(?P<uuid>[a-zA-Z0-9\-]+)/ready/?$', webhooks.whois, name="webhook-whois"),

]
