from django.conf import settings
from urllib.parse import urlparse
from core.models import Url
import base64
import requests

def emitUUIDupdate(uuid, msg):
    """
    Send an update message out to the Redis backend that links to the OtterSockets
    websocket layer.

    :param uuid:
    :param msg:
    :return:
    """
    requests.put(settings.CATFLAP_URL + "update/ui")


def fillContext(opts, request):
    """
    Fill in the basic common data and elements we need for rendering.

    :param opts:
    :param request:
    :return:
    """
    if "request" not in opts:
        opts["request"] = request

    return opts

def resolveIps(uuid, ipv4s):
    """
    Given a block of IP addresses as a list, fire off resolution for them
    :param ipv4s:
    :return:
    """
    for ipv4 in ipv4s:
        blob = {
            "uuid": str(uuid),
            "ip": ipv4
        }
        requests.post(settings.COORDINATOR_URL + "resolve/ip", json=blob)

def commonSearches():
    """
    TODO: Move to a model manager for Url

    select distinct fqdn, id, count(*) as freq from core_url group by fqdn order by freq desc;

    :return:
    """
    return Url.objects.raw(
        """
          select distinct fqdn, id, count(*) as freq
            from core_url
        group by fqdn
        order by freq desc
           limit 10
        """
    )

def recentSearches():
    """
    TODO: Move to a model manager for Url

    select distinct fqdn, max(queriedAt), count(*) as freq from core_url group by fqdn order by queriedAt desc;

    :return:
    """
    return Url.objects.raw(
        """
                select distinct fqdn, id, max(queriedAt), count(*) as freq
                  from core_url
              group by fqdn
              order by queriedAt desc
                limit 10
        """
    )


class OtterUrl(object):
    """
    Wrapper library for manipulating URLs
    """

    def __init__(self, url):
        self.rawUrl = url
        self.parsedUrl = urlparse(self.rawUrl)

        if self.parsedUrl.scheme == "":
            # didn't have a scheme, we need to fix that
            self.rawUrl = "http://" + self.rawUrl.lstrip("/:")
            self.parsedUrl = urlparse(self.rawUrl)

    def fqdn(self):
        return self.parsedUrl.hostname

    def id(self):
        """
        For our purposes the full URL is our id
        :return:
        """
        return self.parsedUrl.geturl()

    def queryBase64(self):
        """
        Generate the URL safe base 64 query that can be used to kick off
        a new query.
        :return:
        """
        return base64.urlsafe_b64encode(bytes(self.rawUrl, "utf8"))

    def createUrlRoot(self, save = True):
        """
        Generate a URL model in our database for this URL
        :return:
        """
        newRoot = Url.objects.create(
            url = self.id(),
            fqdn = self.fqdn()
        )

        if save:
            newRoot.save()

        return newRoot