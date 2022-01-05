from .backend import ProgressSend
from celery import shared_task
import time

@shared_task(bind=True)
def progress_test_task(self):
    progress_send = ProgressSend(self)
    r = 0
    sub = []
    for i in range(10):
        r = r + i
        sub.append({'percentage': (i+1)*10, 'description': (i+1)})
        progress_send.send_progress((i+1)*10, subProgress=sub , description='test')
        time.sleep(1)
    
    return r