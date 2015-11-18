# from django.http import HttpResponse
# from django.template import RequestContext, loader
from django.shortcuts import render

from .models import Project

import datetime

# Each view function takes at least one parameter, called request
def current_datetime(request, uid):
    now = datetime.datetime.now()
    return HttpResponse("<html><body>It is now %s.</body></html>" % now) 


def index(request):
    project_list = Project.objects.order_by('-pid')
    context = {'project_list': project_list}
    return render(request, 'tracker/index.html', context)
    #template = loader.get_template('tracker/index.html')
    #context = RequestContext(request, {
    #    'project_list': project_list,
    #})
    #return HttpResponse(template.render(context))
    

def detail(request, uid):
    return HttpResponse("You're looking at user %s." % uid)


def results(request, uid):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % uid)


def vote(request, uid):
    return HttpResponse("You're voting on user %s." % uid)

