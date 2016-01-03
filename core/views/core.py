from django.shortcuts import render
from core.views import util
from django.contrib import messages

def index(request):
    """
    Setup the basic query templates and layout

    :param request:
    :return:
    """
    opts = {}
    return render(request, "index.html", util.fillContext(opts, request))