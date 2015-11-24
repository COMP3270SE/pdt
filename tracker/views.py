from django.shortcuts import get_object_or_404, render
from django.db.models import Aggregate
from django.db.models import Count, Sum

from .models import Project, Developer, Manager
from .models import Phase, Iteration, Defect
from .models import Workrecord

import datetime

# Each view function takes at least one parameter, called request
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
	if user_id < 50000000:
		raise Http404("You don't have permission to this file")
	else:
		manager = Manager.objects.filter(uid = user_id)
		project = Project.objects.filter(pid = project_id)
		phase_list = Phase.objects.filter(project__pid = project_id)
		iteration_list = Iteration.objects.filter(phase__in = phase_list)

		return render(request, 'tracker/summary.html', {
			'manager': manager, 
			'project': project, 
			'iteration_list': iteration_list,
			'phase_list': phase_list
			#'phase_zip': phase_zip,
			#'project_SLOC': project_SLOC
			})

def timing(request, id):
	return render(request,
                  'tracker/timing.html',
                  {'timing': datetime.datetime.now()})



