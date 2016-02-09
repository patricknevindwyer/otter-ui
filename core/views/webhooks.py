from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from core.models import Url, DnsRecord, AsnRecord, WhoisRecord
import requests
import json

from core.views import util

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
        util.resolveIps(urlModel.uuid, dnsData["result"]["A"])

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
        util.resolveIps(urlModel.uuid, dnsData["result"]["A"])

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
        util.resolveIps(urlModel.uuid, dnsData["result"]["A"])

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
        util.resolveIps(urlModel.uuid, dnsData["result"]["A"])

    return HttpResponse("ok")

def asn(request, uuid):
    """
    Receive the webhook for resolved ASN data. These are triggered from the receipt of
    DNS data, from which we cull IP addresses.

    :param request:
    :param uuid:
    :return:
    """
    urlModel = get_object_or_404(Url, uuid = uuid)

    asnData = processServiceData(settings.SERVICE_ASN_URL, "resolved/%s" % (uuid,))

    if asnData is not None:
        # see if we have any addresses yet, we don't want duplication
        ip = asnData["result"]["ip"]
        existingCount = urlModel.asns.filter(ip=ip, source="asn").count()
        if existingCount == 0:
            asnRecord = AsnRecord.objects.create(
                url = urlModel,
                rawRecord = json.dumps(asnData["result"]),
                ip = ip,
                source = "asn"
            )
            asnRecord.save()

    return HttpResponse("ok")

def whois(request, uuid):
    """
    Receive the webhook for resolved WHOIS data. Whois can be triggered multiple
    time from every URI lookup, so the incoming UUID is not the URI UUID.

    :param request:
    :param uuid:
    :return:
    """

    whoisData = processServiceData(settings.SERVICE_WHOIS_URL, "resolved/%s" % (uuid,))

    if whoisData is not None:

        # pull out the top level UUID
        urlUuid = whoisData["result"]["uuid"]
        isHostLookup = whoisData["result"]["isHostLookup"]
        whoisJson = whoisData["result"]["result"]
        query = whoisData["result"]["query"]

        urlModel = get_object_or_404(Url, uuid = urlUuid)

        if isHostLookup:
            whoisRecord = WhoisRecord.objects.create(
                url = urlModel,
                rawRecord = whoisJson
            )
            whoisRecord.save()

        else:
            # make sure we don't already have this record from WHOIS
            existingCount = urlModel.asns.filter(ip=query, source="whois").count()
            if existingCount == 0:
                # with IP based data we can stash in the Asn format
                asnRecord = AsnRecord.objects.create(
                    url = urlModel,
                    rawRecord = json.dumps(whoisJson),
                    ip = query,
                    source = "whois"
                )
                asnRecord.save()

    return HttpResponse("ok")

