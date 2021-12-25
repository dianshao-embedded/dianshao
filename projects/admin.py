from django.contrib import admin
from .models import ExtraMarco, MyPackages, Project, MetaLayer, Tasks, LocalFile

# Register your models here.

admin.site.register(Project)
admin.site.register(MetaLayer)
admin.site.register(Tasks)
admin.site.register(LocalFile)
admin.site.register(MyPackages)
admin.site.register(ExtraMarco)