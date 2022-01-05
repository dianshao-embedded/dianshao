import json
from celery.result import AsyncResult
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from .backend import ProgressReceive
from .tasks import progress_test_task

# Create your views here.

@never_cache
def get_progress(request, task_id):
    progress = ProgressReceive(AsyncResult(task_id))
    return HttpResponse(json.dumps(progress.get_data()), content_type='application/json')


def progress_test(request):
    result = progress_test_task.delay()
    return render(request, 'progressui/progressbartest.html', context={'task_id': result.task_id})