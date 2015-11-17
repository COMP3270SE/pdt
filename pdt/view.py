# === view ===
# A view function is a Python function that takes a Web request and returns a Web response.

from django.http import HttpResponse, HttpResponseNotFound

import datetime

# Each view function takes at least one parameter, called request
# request: an object that contains info about the current Web request that has triggered this view
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    # if() -> return HttpResponseNotFound('<h1>Page not found</h1>')
    return HttpResponse(html)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def hello(request):
    return HttpResponse("Hello world")

# To hook a view function to a particular URL with Django, use a URLconf.
# See URL dispatcher for instructions.
# === URLconf ===
# A URLconf is like a table of contents for your Django-powered Web site.
# Basically, it’s a mapping between URLs and the view functions that should be called for those URLs.
# It’s how you tell Django, “For this URL, call this code, and for that URL, call that code.”