# === view ===
# A view function is a Python function that takes a Web request and returns a Web response.

from django.http import HttpResponse
from .models import Project

import datetime

# Each view function takes at least one parameter, called request
# request: an object that contains info about the current Web request that has triggered this view
def current_datetime(request, uid):
    now = datetime.datetime.now()
    return HttpResponse("<html><body>It is now %s.</body></html>" % now) 
    
def index(request):
    latest_project_list = Project.objects.order_by('-pid')[:5]
    output = ', '.join([p.description for p in latest_project_list])
    return HttpResponse(output)   
    
def detail(request, uid):
    return HttpResponse("You're looking at user %s." % uid)

def results(request, uid):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % uid)

def vote(request, uid):
    return HttpResponse("You're voting on user %s." % uid)

