# === Manager ===
# tracker/500000000/home.html
# tracker/500000000/project/1/process.html
# tracker/500000000/project/1/people.html
# tracker/500000000/project/1/summary.html

# === Developer ===
# tracker/100000000/home.html
# tracker/100000000/project/1.html
# tracker/100000000/project/1/dev_mode.html
# tracker/100000000/project/1/debug_mode.html
# tracker/100000000/project/1/manage_mode.html
# tracker/100000000/project/1/report.html

# from django.http import HttpResponse
# from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render

from .models import Project, Developer, Manager
from .models import Phase, Iteration, Defect

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
    

def home(request, id):
	if id < 50000000:
		try:
			developer = get_object_or_404(Developer, uid=id)
		except Developer.DoesNotExist:
			raise Http404("Developer does not exist")
		return render(request, 'tracker/home.html', {'user': developer})
	else:
		try:
			manager = get_object_or_404(Manager, uid=id)
		except Manager.DoesNotExist:
			raise Http404("Manager does not exist")
		return render(request, 'tracker/home.html', {'user': manager})

def summary(request, user_id, project_id):
	if id < 50000000:
		raise Http404("You don't have permission to this file")
	else:
		try:
			est_sloc = get_object_or_404(Project, pid = project_id)
			phase_list = Phase.objects.all()
			#phase_list = Phase.objects.filter(project__pid__ = project_id)
			iteration_list = Iteration.objects.filter(phase__in = phase_list)
			iteration_num = len(iteration_list)
		except Project.DoesNotExist:
			raise Http404("Project does not exist")
		return render(request, 'tracker/summary.html', {'est_sloc': est_sloc, 'phase_list': phase_list, 'iteration_list': iteration_list, 'iteration_num': iteration_num})



def results(request, uid):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % uid)


def vote(request, uid):
    return HttpResponse("You're voting on user %s." % uid)

def timing(request, id):
	return render(request,
                  'tracker/timing.html',
                  {'timing': datetime.datetime.now()})



