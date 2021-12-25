from os import name
from django.urls import path
from django.urls.conf import re_path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project, name='project'),
    path('<int:project_id>/initial', views.project_initial, name='initial'),
    path('<int:project_id>/delete', views.project_delete, name='project_delete'),
    path('<int:project_id>/metas', views.metas, name='metas'),
    path('<int:project_id>/meta_create', views.meta_create, name='meta_create'),
    path('<int:project_id>/bitbake', views.bitbake, name='bitbake'),
    path('<int:project_id>/mymeta', views.mymeta, name='mymeta'),
    path('<int:project_id>/myconf', views.myconf, name='myconf'),
    path('<int:project_id>/myconf/<int:myconf_id>', views.myconf_detail, name='myconf_detail'),
    path('<int:project_id>/mypackage_create', views.mypackage_create, name='mypackage_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>', views.mypackage_detail, name='mypackage_detail'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/task_create', views.task_create, name='task_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/extra_marco_create', views.extra_marco_create, name='extra_marco_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file_create', views.file_create, name='file_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file_import', views.file_import, name='file_import'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file_generate_patch', views.file_generate_patch, name='file_generate_patch'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/bbfile', views.mypackage_bbfile, name='mypackage_bbfile'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/bitbake', views.mypackage_bitbake, name='mypackage_bitbake'),
]