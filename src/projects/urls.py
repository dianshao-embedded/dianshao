from os import name
from django.urls import path
from django.urls.conf import re_path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project, name='project'),
    path('import', views.project_import, name='import'),
    path('<int:project_id>/initial', views.project_initial, name='initial'),
    path('<int:project_id>/delete', views.project_delete, name='project_delete'),
    path('<int:project_id>/metas', views.metas, name='metas'),
    path('<int:project_id>/meta_create', views.meta_create, name='meta_create'),
    path('<int:project_id>/bitbake', views.bitbake, name='bitbake'),
    path('<int:project_id>/project_export', views.project_export, name='project_export'),
    path('<int:project_id>/mymeta', views.mymeta, name='mymeta'),
    path('<int:project_id>/mypackage_create', views.mypackage_create, name='mypackage_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>', views.mypackage_detail, name='mypackage_detail'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/delete', views.mypackage_delete, name='mypackage_delete'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/task_create', views.task_create, name='task_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/task/<int:task_id>/delete', views.task_delete, name='task_delete'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/install_task_create', views.install_task_create, name='install_task_create'),    
    path('<int:project_id>/mypackage/<int:mypackage_id>/extra_marco_create', views.extra_marco_create, name='extra_marco_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/macro/<int:macro_id>/delete', views.extra_macro_delete, name='extra_marco_delete'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file/<int:file_id>/delete', views.file_delete, name='file_delete'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file_create', views.file_create, name='file_create'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file_import', views.file_import, name='file_import'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/file_generate_patch', views.file_generate_patch, name='file_generate_patch'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/bbfile', views.mypackage_bbfile, name='mypackage_bbfile'),
    path('<int:project_id>/mypackage/<int:mypackage_id>/bitbake', views.mypackage_bitbake, name='mypackage_bitbake'),
    path('<int:project_id>/mymachine_create', views.mymachine_create, name='mymachine_create'),
    path('<int:project_id>/mymachine/<int:mymachine_id>/extra_marco_create', views.extra_machine_marco_create, name='extra_machine_marco_create'),
    path('<int:project_id>/mypackage/<int:mymachine_id>/file', views.mymachine_file, name='mymachine_file'),
    path('<int:project_id>/myimage_create', views.myimage_create, name='myimage_create'),
    path('<int:project_id>/myconf_update', views.myconf_update, name='myconf_update'),
    path('<int:project_id>/myimage/<int:myimage_id>', views.myimage_detail, name='myimage_detail'),
    path('<int:project_id>/myimage/<int:myimage_id>/delete', views.myimage_delete, name='myimage_delete'),
    path('<int:project_id>/myimage/<int:myimage_id>/extra_marco_create', views.image_extra_marco_create, name='image_extra_marco_create'),
    path('<int:project_id>/myimage/<int:myimage_id>/macro/<int:macro_id>/delete', views.image_extra_macro_delete, name='image_extra_macro_delete'),
    path('<int:project_id>/myimage/<int:myimage_id>/file', views.myimage_file, name='myimage_file'),
    path('<int:project_id>/myimage/<int:myimage_id>/bitbake', views.myimage_bitbake, name='myimage_bitbake'),
    path('<int:project_id>/myimage/<int:myimage_id>/add_wks_file', views.add_wks_file, name='add_wks_file'),
    path('<int:project_id>/mymachine', views.mymachine, name='mymachine'),
    path('<int:project_id>/mypackages', views.mypackages, name='mypackages'),
    path('<int:project_id>/myimages', views.myimages, name='myimages'),
    #path('<int:project_id>/myimage/<int:myimage_id>/uboot_bitbake', views.uboot_bitbake, name='uboot_bitbake'),
    #path('<int:project_id>/myimage/<int:myimage_id>/kernel_bitbake', views.kernel_bitbake, name='kernel_bitbake'),
    #path('<int:project_id>/myimage/<int:myimage_id>/image_bitbake', views.image_bitbake, name='image_bitbake'),
]