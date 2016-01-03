from django.shortcuts import render
from core.views import util

def search(request):
    """
    Taking the incoming search query, either pull up the existing info for
    the FQDN, or kick off a new search.

    :param request:
    :return:
    """
    opts = {}
    return render(request, "index.html", util.fillContext(opts, request))

