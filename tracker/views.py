from django.shortcuts import get_object_or_404, render, render_to_response
from django.db.models import Aggregate
from django.db.models import Count, Sum
from django.db.models import Q

from django.template.context_processors import csrf

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Project, Developer, Manager
from .models import Phase, Iteration, Defect
from .models import Workrecord

from django import forms
from django.http import HttpResponse
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
 
def userlogin(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # username = request.POST.get("username", "Guest")
        # password = request.POST.get("password", "Guest")
        user = authenticate(username=username, password=password)
        if user is not None:            
                login(request, user)                
                if user.user_type=='M':
                	return HttpResponseRedirect('/tracker/manager/'+str(user.pk)+'/home')
                else:
           			return HttpResponseRedirect('/tracker/developer/'+str(user.pk)+'/home')
        else:
            # Return an 'invalid login' error message.
            print HttpResponse('Incorrect username or password.')
    return render(request, 'tracker/login.html', {})
       
@login_required(login_url='/tracker')
def developerhome(request, user_id):

        try:
            user = get_object_or_404(Developer, account__pk = user_id)
            project_list = Project.objects.filter(developer__account__pk = user_id)
        except Developer.DoesNotExist:
            raise Http404("Developer does not exist")
        return render(request, 'tracker/home.html', {
            'user': user,
            'project_list': project_list,
            'isManager': False
            })

@login_required(login_url='/tracker')
def managerhome(request, user_id):
        try:
            user = get_object_or_404(Manager, account__pk = user_id)
            project_list = Project.objects.filter(manager__account__pk = user_id)
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

@login_required(login_url='/tracker')   
def createproject(request, user_id):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/tracker/manager/'+user_id+'/home/')

	form = ProjectForm()
	user = get_object_or_404(Manager, account__pk = user_id)
	return render(request, 'tracker/createproject.html', {
    	'form': form,
    	'user': user
    	})

@login_required(login_url='/tracker')
def viewproject(request, user_id, project_id):
	user = get_object_or_404(Manager, account__pk = user_id)
	project = get_object_or_404(Project, pk = project_id)
	phase_list = Phase.objects.filter(project__pk = project_id).order_by('type')
	iteration_list = Iteration.objects.filter(phase__in = phase_list).order_by('pk')
	active_iteration = get_object_or_404(Iteration, status = 1, phase__project__pk = project_id)
	if Iteration.objects.filter(~Q(status=0)).count() > 0:
		is_opened_iteration = True
	else:
		is_opened_iteration = False

	return render(request, 'tracker/project_index.html', {
		'user': user,
		'phase_list': phase_list,
		'iteration_list': iteration_list,
		'project': project,
		'active_iteration': active_iteration,
		'is_opened_iteration': is_opened_iteration
		})

class IterationForm(forms.ModelForm):
	class Meta:
		model = Iteration
		fields = ['iteration_id', 'status']

def changeItState(request, user_id, project_id, iteration_id):
	if request.method == 'POST':
		it_form = IterationForm(request.POST)

	if it_form.is_valid():
		iteration = Iteration.objects.get(pk=iteration_id)
		it_form = IterationForm(request.POST, instance = iteration)
		it_form.save()
		return HttpResponseRedirect('/tracker/'+user_id+'/project/'+project_id)
	else:
		iteration = Iteration.objects.get(pk = iteration_id)       
		it_form = Iteration(instance=iteration)

        return render_to_response('tracker/project_index.html',{'form':it_form}, context_instance=RequestContext(request))

@login_required(login_url='/tracker')
def summary(request, user_id, project_id):
		manager = get_object_or_404(Manager, account__pk = user_id)
		project = get_object_or_404(Project, pk = project_id)
		phase_list = Phase.objects.filter(project__pk = project_id)
		iteration_list = Iteration.objects.filter(phase__in = phase_list)

		return render(request, 'tracker/summary.html', {
			'manager': manager, 
			'project': project, 
			'iteration_list': iteration_list,
			'phase_list': phase_list
			})

def timing(request, user_id, project_id):
    developer = get_object_or_404(Developer, account__pk = user_id)
    active_iteration = get_object_or_404(Iteration, status = 1, phase__project__pk = project_id)
    defect_list = Defect.objects.filter(in_iteration__phase__project__pk = project_id)
    return render(request, 'tracker/timing.html', {
        'developer': developer, 
        'active_iteration': active_iteration, 
        'defect_list': defect_list,
        })

@login_required(login_url='/tracker')
def people(request, user_id, project_id):
	project = get_object_or_404(Project, pk = project_id)
	user = get_object_or_404(Manager, account__pk = user_id)
	developer_list = project.developer.all()
	return render(request, 'tracker/people.html', {
		'developer_list': developer_list,
		'user': user,
		'project': project
		})

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

def workonproject(request, user_id, project_id):
    return render(request, 'tracker/project_work.html', {})
