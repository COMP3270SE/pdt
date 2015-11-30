import datetime

from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count, Sum
from django.contrib.auth.models import AbstractUser

########
# Many-to-one: iteration - phase, phase - project, project - manager,
#              defect - developer, defect - iteration
# Mant-to-many: developer - project,
# One-to-one:

class Account (AbstractUser):
    type_choices = (
        ('SU', 'Super User'),
        ('M', 'Manager'),
        ('D', 'Developer'),
    )
    user_type = models.CharField(max_length=2,
                                 choices=type_choices,
                                 default='M')
    def __unicode__(self):
        return str(self.pk)+":"+self.username

class Manager(models.Model):
    account = models.OneToOneField(Account)
    #uid = models.IntegerField(validators=[MinValueValidator(50000000), MaxValueValidator(99999999)], primary_key=True)
    #name = models.CharField(max_length=100)
    #password = models.CharField(max_length=20)
    
    def __unicode__(self):
        return str(self.account.username)

class Developer(models.Model):
    account = models.OneToOneField(Account)
    #uid = models.IntegerField(validators=[MinValueValidator(10000000), MaxValueValidator(49999999)], primary_key=True)
    #name = models.CharField(max_length=100)
    #password = models.CharField(max_length=20)
    
    def __unicode__(self):
        return str(self.account.username)

class Project(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager)
    developer = models.ManyToManyField(Developer)
    est_SLOC = models.IntegerField(default=0)
    est_escape = models.FloatField(default=0.0)
    est_effort = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.name
    
    @property
    def SLOC(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self)
        return iteration_list.aggregate(sum = Sum('SLOC'))

    @property
    def SLOC_percent(self):
        divider = self.est_SLOC;
        if divider == 0:
            return "NA"
        return round(100*self.SLOC['sum']/divider, 2)

    @property
    def effort(self):
        phase_list = Phase.objects.filter(project=self)
        effort = 0
        for phase in phase_list:
            effort += phase.effort
        return round(effort, 2)

    @property
    def effort_percent(self):
        divider = self.est_effort;
        if divider == 0:
            return "NA"
        return round(100*self.effort/divider, 2)

    @property
    def SLOC_effort(self):
        divider = self.effort
        if divider == 0:
            return "NA"
        return round(self.SLOC['sum']/divider, 2)

    @property
    def SLOC_effort_percent(self):
        if self.est_effort == 0:
            return "NA"
        divider = self.est_SLOC/self.est_effort;
        if divider == 0:
            return "NA"
        return round(100*self.SLOC_effort/divider, 2)

    @property
    def defect_in(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self)
        return Defect.objects.filter(injection_iteration__in = iteration_list).count()

    @property
    def defect_out(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self)
        return Defect.objects.filter(removal_iteration__in = iteration_list).count()

    @property
    def defect_in_rate(self):
        divider = self.effort
        if divider == 0:
            return "NA"
        return round(self.defect_in/divider, 2)

    @property
    def defect_out_rate(self):
        divider = self.effort
        if divider == 0:
            return "NA"
        return round(self.defect_out/divider, 2)

    @property
    def defect_density(self):
        return float(self.defect_in)/ float(1000*self.SLOC['sum'])

    @property
    def defect_escape(self):
        iteration_list = Iteration.objects.filter(phase__project = self).order_by('-iteration_id')
        return iteration_list[0].defect_in * self.est_escape

    @property
    def defect_yield(self):
        divider = self.defect_in+self.defect_escape
        if divider == 0:
            return "NA"
        return round(1-self.defect_escape/divider, 2)


class Phase(models.Model):
    type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    phase_id = models.AutoField(primary_key = True)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        if self.type == 1:
	        return self.project.name + ": Inception Phase"
        elif self.type == 2:
	    	return self.project.name + ": Elaboration Phase"
        elif self.type == 3:
	    	return self.project.name + ": Construction Phase"
        else:
	    	return self.project.name + ": Transition Phase"
    
    @property
    def SLOC(self):
        return Iteration.objects.filter(phase = self).aggregate(sum = Sum('SLOC'))

    @property
    def SLOC_percent(self):
        divider = self.project.est_SLOC
        if divider == 0:
            return "NA"
        return round(100*self.SLOC['sum']/divider, 2)

    @property
    def effort(self):
        iteration_list = Iteration.objects.filter(phase = self)
        effort = 0
        for iteration in iteration_list:
            effort += iteration.effort
        return round(effort, 2)

    @property
    def effort_percent(self):
        divider = self.project.est_effort;
        if divider == 0:
            return "NA"
        return round(100*self.effort/divider, 2)

    @property
    def SLOC_effort(self):
        if self.effort == 0:
            return "NA"
        return round(self.SLOC['sum']/self.effort)

    @property
    def SLOC_effort_percent(self):
        if self.project.est_SLOC == 0:
            return "NA"
        if self.project.est_effort == 0:
            return "NA"
        divider = self.project.est_SLOC/self.project.est_effort
        if divider == 0:
            return "NA"
        return round(100*self.SLOC_effort/divider, 2)

    @property
    def defect_in(self):
        iteration_list = Iteration.objects.filter(phase = self)
        return Defect.objects.filter(injection_iteration__in = iteration_list).count()

    @property
    def defect_out(self):
        iteration_list = Iteration.objects.filter(phase = self)
        return Defect.objects.filter(removal_iteration__in = iteration_list).count()

    @property
    def defect_in_rate(self):
        if self.effort == 0:
            return "NA"
        return round(self.defect_in/self.effort, 2)

    @property
    def defect_out_rate(self):
        if self.effort == 0:
            return "NA"
        return round(self.defect_out/self.effort, 2)

    @property
    def defect_density(self):
        divider = float(1000*self.SLOC['sum'])
        if divider == 0:
            return "NA"
        return float(self.defect_in)/ divider

    @property
    def defect_in_total(self):
        phase_list = Phase.objects.filter(project = self.project).filter(phase_id__lte=self.phase_id)
        total = 0
        for i in phase_list:
            total += i.defect_in
        return total

    @property
    def defect_out_total(self):
        phase_list = Phase.objects.filter(project = self.project).filter(phase_id__lt=self.phase_id)
        total = 0
        for i in phase_list:
            total += i.defect_out
        return total

    @property
    def defect_yield(self):
        escape_rate = Project.objects.filter(pid = self.project.pid)[0].est_escape
        last_phase = Phase.objects.filter(project = self.project).order_by('-phase_id')[0]
        defect_escape = escape_rate * Defect.objects.filter(injection_iteration__phase=self, removal_iteration__phase=last_phase).count()
        pre_defect_out_total = self.defect_out_total
        divider = defect_escape + self.defect_in_total - pre_defect_out_total
        if divider == 0:
            return "NA"
        return round(self.defect_out/divider, 2)


class Iteration(models.Model):
    SLOC = models.IntegerField(default=0)
    iteration_id = models.AutoField(primary_key = True)
    time_length = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phase = models.ForeignKey(Phase)
       
    def __unicode__(self):
        return self.name

    @property
    def SLOC_percent(self):
        divider = self.phase.project.est_SLOC
        if divider == 0:
            return "NA"
        return round(100*self.SLOC/divider, 2)

    @property
    def effort(self):
        record_list = Workrecord.objects.filter(iteration = self)
        effort = 0
        for record in record_list:
            effort += record.duration
        return round(effort, 2)

    @property
    def effort_percent(self):
        divider = self.phase.project.est_effort
        if divider == 0:
            return "NA"
        return round(100*self.effort/divider, 2)

    @property
    def SLOC_effort(self):
        if self.effort == 0:
            return "NA"
        return round(self.SLOC/self.effort, 2)

    @property
    def SLOC_effort_percent(self):
        if self.phase.project.est_SLOC == 0:
            return "NA"
        if self.phase.project.est_effort == 0:
            return "NA"
        divider = self.phase.project.est_SLOC/self.phase.project.est_effort
        if divider == 0:
            return "NA"
        return round(100*self.SLOC_effort/divider, 2)


    @property
    def defect_in(self):
        return Defect.objects.filter(injection_iteration = self).count()

    @property
    def defect_out(self):
        return Defect.objects.filter(removal_iteration = self).count()

    @property
    def defect_in_rate(self):
        if self.effort == 0:
            return "NA"
        return round(self.defect_in/self.effort, 2)

    @property
    def defect_out_rate(self):
        if self.effort == 0:
            return "NA"
        return round(self.defect_out/self.effort, 2)

    @property
    def defect_density(self):
        return float(self.defect_in)/ float(1000*self.SLOC)

    @property
    def defect_in_total(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self.phase.project).filter(iteration_id__lte=self.iteration_id)
        total = 0
        for i in iteration_list:
            total += i.defect_in
        return total

    @property
    def defect_out_total(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self.phase.project).filter(iteration_id__lt=self.iteration_id)
        total = 0
        for i in iteration_list:
            total += i.defect_out
        return total

    @property
    def defect_yield(self):
        escape_rate = Project.objects.filter(pid = self.phase.project.pid)[0].est_escape
        last_iteration = Iteration.objects.filter(phase__project__exact = self.phase.project).order_by('-iteration_id')[0]
        defect_escape = escape_rate * Defect.objects.filter(injection_iteration = self, removal_iteration=last_iteration).count()
        pre_defect_out_total = self.defect_out_total
        divider = defect_escape + self.defect_in_total - pre_defect_out_total
        if divider == 0:
            return "NA"
        return round(self.defect_out/divider, 2)


class Defect(models.Model):
    did = models.IntegerField(default=0, primary_key=True)
    type = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    injection_iteration = models.ForeignKey(Iteration, related_name='injection', default=1)
    removal_iteration = models.ForeignKey(Iteration, related_name='removal', default=1)
    developer = models.ForeignKey(Developer) 
    
    def __unicode__(self):
        return str(self.did)+"-"+str(self.type)+": injection-"+str(self.injection_iteration)+", removal-"+str(self.removal_iteration)

class Workrecord(models.Model):
    wid = models.AutoField(primary_key=True)
    #starttime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    #endtime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    interval = models.FloatField(default=0.0)
    developer = models.ForeignKey(Developer)
    iteration = models.ForeignKey(Iteration)
    def __unicode__(self):
        return str(self.wid)+"by"+str(self.developer.account.username)
    
    @classmethod
    def create(cls, interval, developer, iteration):
        book = cls(interval=interval, developer= developer, iteration= iteration)
        return book

    @property
    def duration(self):
        #return (self.endtime-self.starttime).total_seconds()/3600
        return  self.interval




