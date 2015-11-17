import datetime

from django.db import models
from django.utils import timezone

# Each model has a number of class variables representing a database field in the model.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        # customised method
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


########
# Many-to-one: iteration - phase, phase - project, project - manager,
#              defect - developer, defect - iteration
# Mant-to-many: developer - project,
# One-to-one:

class Manager(models.Model):
    uid = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name

class Developer(models.Model):
    uid = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name

class Project(models.Model):
    pid = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    manager = models.ForeignKey(Manager)
    developer = models.ManyToManyField(Developer)

    def __unicode__(self):
        return self.name

class Phase(models.Model):
    type = models.IntegerField(default=1)
    project = models.ForeignKey(Project)
    
    def __unicode__(self):
        return self.type

class Iteration(models.Model):
    SLOC = models.IntegerField(default=0)
    effort = models.IntegerField(default=0)
    time_length = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    phase = models.ForeignKey(Phase)
    
    def __unicode__(self):
        return self.name

class Defect(models.Model):
    type = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    iteration = models.ForeignKey(Iteration)
    developer = models.ForeignKey(Developer)
    
    def __unicode__(self):
        return self.type




