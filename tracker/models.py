import datetime

from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count, Sum

########
# Many-to-one: iteration - phase, phase - project, project - manager,
#              defect - developer, defect - iteration
# Mant-to-many: developer - project,
# One-to-one:

class Manager(models.Model):
    uid = models.IntegerField(validators=[MinValueValidator(50000000), MaxValueValidator(99999999)], primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name

class Developer(models.Model):
    uid = models.IntegerField(validators=[MinValueValidator(10000000), MaxValueValidator(49999999)], primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name

class Project(models.Model):
    pid = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager)
    developer = models.ManyToManyField(Developer)
    est_SLOC = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
    
    @property
    def SLOC(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self)
        return iteration_list.aggregate(sum = Sum('SLOC'))

    @property
    def effort(self):
        phase_list = Phase.objects.filter(project=self)
        effort = 0
        for phase in phase_list:
            effort += phase.effort
        return round(effort, 2)

    @property
    def SLOC_effort(self):
        return round(self.SLOC['sum']/self.effort, 2)

    @property
    def defect_in(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self)
        return Defect.objects.filter(in_iteration__in = iteration_list).count()

    @property
    def defect_out(self):
        iteration_list = Iteration.objects.filter(phase__project__exact = self)
        return Defect.objects.filter(out_iteration__in = iteration_list).count()

    @property
    def defect_in_rate(self):
        return round(self.defect_in/self.effort, 2)

    @property
    def defect_out_rate(self):
        return round(self.defect_out/self.effort, 2)

    @property
    def defect_density(self):
        return float(self.defect_in)/ float(1000*self.SLOC['sum'])

class Phase(models.Model):
    type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    phase_id = models.IntegerField(default=0, primary_key = True)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        if self.type == 1:
	        return self.project.name + ": P1"
        elif self.type == 2:
	    	return self.project.name + ": P2"
        elif self.type == 3:
	    	return self.project.name + ": P3"
        else:
	    	return self.project.name + ": P4"
    
    @property
    def SLOC(self):
        return Iteration.objects.filter(phase = self).aggregate(sum = Sum('SLOC'))

    @property
    def effort(self):
        iteration_list = Iteration.objects.filter(phase = self)
        effort = 0
        for iteration in iteration_list:
            effort += iteration.effort
        return round(effort, 2)

    @property
    def SLOC_effort(self):
        return round(self.SLOC['sum']/self.effort)

    @property
    def defect_in(self):
        iteration_list = Iteration.objects.filter(phase = self)
        return Defect.objects.filter(in_iteration__in = iteration_list).count()

    @property
    def defect_out(self):
        iteration_list = Iteration.objects.filter(phase = self)
        return Defect.objects.filter(out_iteration__in = iteration_list).count()

    @property
    def defect_in_rate(self):
        return round(self.defect_in/self.effort, 2)

    @property
    def defect_out_rate(self):
        return round(self.defect_out/self.effort, 2)

    @property
    def defect_density(self):
        return float(self.defect_in)/ float(1000*self.SLOC['sum'])

class Iteration(models.Model):
    SLOC = models.IntegerField(default=0)
    iteration_id = models.IntegerField(default=0, primary_key = True)
    time_length = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phase = models.ForeignKey(Phase)
       
    def __unicode__(self):
        return self.name

    @property
    def effort(self):
        record_list = Workrecord.objects.filter(iteration = self)
        effort = 0
        for record in record_list:
            effort += record.duration
        return round(effort, 2)

    @property
    def SLOC_effort(self):
        return round(self.SLOC/self.effort, 2)

    @property
    def defect_in(self):
        return Defect.objects.filter(in_iteration = self).count()

    @property
    def defect_out(self):
        return Defect.objects.filter(out_iteration = self).count()

    @property
    def defect_in_rate(self):
        return round(self.defect_in/self.effort, 2)

    @property
    def defect_out_rate(self):
        return round(self.defect_out/self.effort, 2)

    @property
    def defect_density(self):
        return float(self.defect_in)/ float(1000*self.SLOC)

class Defect(models.Model):
    did = models.IntegerField(default=0, primary_key=True)
    type = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    in_iteration = models.ForeignKey(Iteration, related_name='injection', default=1)
    out_iteration = models.ForeignKey(Iteration, related_name='removal', default=1)
    developer = models.ForeignKey(Developer) 
    
    def __unicode__(self):
        return str(self.did)+"-"+str(self.type)+": in-"+str(self.in_iteration)+", out-"+str(self.out_iteration)

class Workrecord(models.Model):
    wid = models.IntegerField(default=0, primary_key=True)
    starttime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    endtime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    developer = models.ForeignKey(Developer)
    iteration = models.ForeignKey(Iteration)
    def __unicode__(self):
        return str(self.wid)+self.developer.name
    
    @property
    def duration(self):
        return (self.endtime-self.starttime).total_seconds()/3600
        #return (self.endtime-self.starttime).days