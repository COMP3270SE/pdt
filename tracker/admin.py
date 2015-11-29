from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Account)
admin.site.register(Manager)
admin.site.register(Developer)
admin.site.register(Project)
admin.site.register(Phase)
admin.site.register(Iteration)
admin.site.register(Defect)
admin.site.register(Workrecord)