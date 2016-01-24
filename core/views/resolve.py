from django.shortcuts import render
from core.views import util
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

import base64
import requests

from core.models import Url

def start(request, url):
    """
    Start the resolve process by creating a new Otter URL object. This also
    kicks off the entire lookup process. This endpoint will trigger a redirect
    to the resolve/<id>/ endpoint.

    :param request:
    :param url: Base64'd full URL of the resolve target
    :return:
    """
    realUrl = base64.urlsafe_b64decode(url).decode("utf8")
    print("starting resolve process\n\tb64: [%s]\n\tstr: [%s]" % (url, realUrl))

    # create the new object
    otterUrl = util.OtterUrl(realUrl)
    newResolveUrl = otterUrl.createUrlRoot(save=True)

    requests.post(settings.COORDINATOR_URL + "resolve", json=newResolveUrl.json())

    return HttpResponseRedirect(reverse("lookup-details", args=(str(newResolveUrl.uuid),)))

def details(request, url_id):
    """

    :param request:
    :param url_id:
    :return:
    """
    url = Url.objects.filter(uuid=url_id).first()
    opts = {
        "url": url
    }
    return render(request, "details.html", util.fillContext(opts, request))