from django.http import HttpResponse
from django.shortcuts import render

def ack(request):
    """

    :param request:
    :return:
    """
    return HttpResponse("hello")