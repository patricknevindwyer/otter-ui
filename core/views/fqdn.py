from django.shortcuts import render
from core.views import util
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from core.models import Url

def details(request, fqdn):
    """
    Build up some details on the FQDN in question.

    :param request:
    :param fqdn:
    :return:
    """

    opts = {
        "fqdn": fqdn,
        "resolves": Url.objects.filter(fqdn = fqdn).order_by("-queriedAt")
    }
    return render(request, "fqdn.html", util.fillContext(opts, request))