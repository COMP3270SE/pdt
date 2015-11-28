from django.shortcuts import get_object_or_404, render, render_to_response
from django.db.models import Aggregate
from django.db.models import Count, Sum

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

from .models import Project, Developer, Manager
from .models import Phase, Iteration, Defect
from .models import Workrecord

from django import forms
from django.http import HttpResponseRedirect
import datetime

# Each view function takes at least one parameter, called request
def index(request, project_id):
    phase_list = Phase.objects.filter(project__pk = project_id).order_by('pk')
    iteration_list = Iteration.objects.filter(phase__in = phase_list).order_by('pk')
    context = {'phase_list': project_list, 'iteration_list': iteration_list}
    return render(request, 'tracker/index.html', context)
    #template = loader.get_template('tracker/index.html')
    #context = RequestContext(request, {
    #    'project_list': project_list,
    #})
    #return HttpResponse(template.render(context))
    
def home(request, user_id):
	if user_id < 50000000:
		try:
			user = get_object_or_404(Developer, pk = user_id)
			project_list = Project.objects.filter(developer__pk = user_id)
		except Developer.DoesNotExist:
			raise Http404("Developer does not exist")
		return render(request, 'tracker/home.html', {
			'user': user,
			'project_list': project_list,
			'isManager': False
			})
	else:
		try:
			user = get_object_or_404(Manager, pk = user_id)
			project_list = Project.objects.filter(manager__pk = user_id)
		except Manager.DoesNotExist:
			raise Http404("Manager does not exist")
		return render(request, 'tracker/home.html', {
			'user': user,
			'project_list': project_list,
			'isManager': True
			})

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'manager', 'developer', 'est_SLOC', 'est_escape']
    
def createproject(request, user_id):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tracker/'+user_id+'/home/')

    form = ProjectForm()
    return render(request, 'tracker/createproject.html', {'form': form})

def summary(request, user_id, project_id):
	if user_id < 50000000:
		raise Http404("You don't have permission to this file")
	else:
		manager = Manager.objects.filter(pk = user_id)
		project = Project.objects.filter(pk = project_id)
		phase_list = Phase.objects.filter(project__pk = project_id)
		iteration_list = Iteration.objects.filter(phase__in = phase_list)

		return render(request, 'tracker/summary.html', {
			'manager': manager, 
			'project': project, 
			'iteration_list': iteration_list,
			'phase_list': phase_list
			})

def timing(request, id):
	return render(request,
                  'tracker/timing.html',
                  {})

def people(request, user_id, project_id):
	return render(request, 'tracker/people.html', {})

class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = ['type', 'description', 'in_iteration', 'out_iteration', 'developer']
    
def reportDefect(request, id):
    if request.method == 'POST':
        form = DefectForm(request.POST)
        if form.is_valid():
            new_defect = form.save()
            return HttpResponseRedirect('/tracker/Defect/' + str(new_defect.pk))

    form = DefectForm()
    return render(request, 'tracker/reportdefect.html', {'form': form})

def showDefect(request, defect_id):
	return render(request, 'tracker/showdefect.html', {})

