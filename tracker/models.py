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
    
    @property
    def get_effort(self):
        phase_list = Phase.objects.filter(project=self)
        effort = 0
        for phase in phase_list:
            effort += phase.get_effort()
        return effort

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
    def get_effort(self):
        iteration_list = Iteration.objects.filter(phase__phase_id = self.phase_id)
        effort = 0
        for iteration in iteration_list:
            effort += iteration.get_effort()
        return effort

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
    def get_effort(self):
        record_list = Workrecord.objects.filter(iteration__iteration_id = self.iteration_id)
        effort = 0
        for record in record_list:
            effort += record.getDuration()
        return effort


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
    
    @property
    def get_duration(self):
        return self.endtime-self.starttime
 



'''

@property
    def total(self):
        return self.qty * self.cost

        

However, if what you actually want to do is to add a method that does a queryset-level operation, 
like objects.filter() or objects.get(), then your best bet is to define a custom Manager and add 
your method there. Then you will be able to do model.objects.my_custom_method(). Again, see the 
Django documentation on Managers.

class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.id, p.question, p.poll_date, COUNT(*)
            FROM polls_opinionpoll p, polls_response r
            WHERE p.id = r.poll_id
            GROUP BY p.id, p.question, p.poll_date
            ORDER BY p.poll_date DESC""")
        result_list = []
        for row in cursor.fetchall():
            p = self.model(id=row[0], question=row[1], poll_date=row[2])
            p.num_responses = row[3]
            result_list.append(p)
        return result_list
'''
             


