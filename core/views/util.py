

def fillContext(opts, request):
    if "request" not in opts:
        opts["request"] = request

    return opts