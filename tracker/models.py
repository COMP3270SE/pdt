import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Iteration(models.Model):
    SLOC = models.IntegerField(default=0)
    iteration_id = models.IntegerField(default=0, primary_key = True)
    effort = models.IntegerField(default=0)
    time_length = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phase = models.ForeignKey(Phase)
       
    def __unicode__(self):
        return self.name

class Defect(models.Model):
    did = models.IntegerField(default=0, primary_key=True)
    type = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    iteration = models.ForeignKey(Iteration)
    developer = models.ForeignKey(Developer) 
    
    def __unicode__(self):
        return str(self.id)+"-"+self.type

class Workrecord(models.Model):
    wid = models.IntegerField(default=0, primary_key=True)
    starttime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    endtime = models.DateTimeField(default=datetime.datetime.now, blank=True)
    developer = models.ForeignKey(Developer)
    iteration = models.ForeignKey(Iteration)
    def __unicode__(self):
        return self.developer.name+str(wid)
    def duration(self):
        return self.endtime-self.starttime
                


