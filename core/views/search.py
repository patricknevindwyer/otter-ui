from django.shortcuts import render
from core.views import util
from core.models import Url

def search(request):
    """
    Taking the incoming search query, either pull up the existing info for
    the FQDN, or kick off a new search. Or find all queries that have been done
    for this URL.

    :param request:
    :return:
    """
    opts = {}

    # make sure we got a query param
    if not "query" in request.POST:
        return render(request, "index.html", util.fillContext(opts, request))
    else:

        rawUrl = request.POST.get("query")

        # see if we have this search term yet
        otterUrl = util.OtterUrl(rawUrl)

        # try and look this up
        queryRoot = Url.objects.filter(url = otterUrl.id()).order_by("-queriedAt").all()

        opts["matches"] = queryRoot
        opts["query"] = otterUrl

        return render(request, "search.html", util.fillContext(opts, request))

