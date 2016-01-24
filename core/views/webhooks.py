from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from core.models import Url, DnsRecord
import requests
import json

def processServiceData(service, path, delete = True, asJson = True):
    """
    Retrieve data from a remote webhook service endpoint, and possibly trigger the
    remote delete of the cached data. Return the data.

    :param service:
    :param path:
    :param delete:
    :return: JSON or Text of the webhooked service response
    """
    resolvedData = requests.get(service + path)
    if resolvedData.status_code == 200:
        if delete:
            requests.delete(service + path)
        if asJson:
            return resolvedData.json()
        else:
            return resolvedData.text
    else:
        return None


def dns(request, uuid):
    """
    Receive the webhook ping from the DNS resolver. The return data is stored directly
    into the URL model for now. This DNS info is always queried from the network, not
    from getaddrinfo (see cachedDns below).

    :param request: request context
    :param uuid: request UUID
    :return:
    """
    urlModel = get_object_or_404(Url, uuid = uuid)

    dnsData = processServiceData(settings.SERVICE_DNS_URL, "resolved/%s" % (uuid,))

    if dnsData is not None:
        dnsRecord = DnsRecord.objects.create(
            url = urlModel,
            source = "network",
            rawRecord = json.dumps(dnsData["result"])
        )
        dnsRecord.save()

    return HttpResponse("ok")

def cachedDns(request, uuid):
    """
    Recieve DNS info for a resolve target as if the DNS was resolved using the
    server local getaddrinfo(3).

    :param request: request context
    :param uuid: request UUID
    :return:
    """
    urlModel = get_object_or_404(Url, uuid = uuid)

    dnsData = processServiceData(settings.SERVICE_CACHEDDNS_URL, "resolved/%s" % (uuid,))

    if dnsData is not None:
        dnsRecord = DnsRecord.objects.create(
            url = urlModel,
            source = "getaddrinfo",
            rawRecord = json.dumps(dnsData["result"])
        )
        dnsRecord.save()

    return HttpResponse("ok")

def googleDns(request, uuid):
    """
    Receive resolved DNS data from Google's Public DNS service. This is a network based
    lookup.

    :param request:
    :param uuid:
    :return:
    """
    urlModel = get_object_or_404(Url, uuid = uuid)

    dnsData = processServiceData(settings.SERVICE_GOOGLEDNS_URL, "resolved/%s" % (uuid,))

    if dnsData is not None:
        dnsRecord = DnsRecord.objects.create(
            url = urlModel,
            source = "Google Public DNS",
            rawRecord = json.dumps(dnsData["result"])
        )
        dnsRecord.save()

    return HttpResponse("ok")

def openNicDns(request, uuid):
    """
    Receive resolved DNS data from OpenNIC's Public DNS service. This is a network based
    lookup.

    :param request:
    :param uuid:
    :return:
    """
    urlModel = get_object_or_404(Url, uuid = uuid)

    dnsData = processServiceData(settings.SERVICE_OPENNICDNS_URL, "resolved/%s" % (uuid,))

    if dnsData is not None:
        dnsRecord = DnsRecord.objects.create(
            url = urlModel,
            source = "OpenNIC DNS",
            rawRecord = json.dumps(dnsData["result"])
        )
        dnsRecord.save()

    return HttpResponse("ok")

