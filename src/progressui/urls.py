from django.urls import path

from . import views

app_name = 'progressui'

urlpatterns = [
    path('test', views.progress_test, name='progresstest'),
    path('<task_id>', views.get_progress, name='progress'),
]