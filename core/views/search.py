from django.shortcuts import render
from core.views import util
from core.models import Url
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
        return HttpResponseRedirect(reverse("index"))
    else:

        rawUrl = request.POST.get("query")

        # see if we have this search term yet
        otterUrl = util.OtterUrl(rawUrl)

        # TODO: This is just... fucking broken as hell. Needs to be a real query, with
        #       real mappings, and real search...

        # try and look this up
        #queryRoot = Url.objects.raw(
        #    """
        #      select distinct fqdn, id, count(*) as freq, queriedAt
        #        from core_url
        #       where fqdn = "%s"
        #    group by fqdn
        #    order by queriedAt desc
        #    """,
        #    otterUrl.id()
        #)
        queryRoot = [Url.objects.filter(url = otterUrl.id()).order_by("-queriedAt").first()]
        queryCount = Url.objects.filter(url = otterUrl.id()).count()

        # first time queries have no history
        if None in queryRoot:
            queryRoot.remove(None)

        opts["matches"] = queryRoot
        opts["query"] = otterUrl
        opts["queryCount"] = queryCount

        print (queryRoot)
        return render(request, "search.html", util.fillContext(opts, request))

