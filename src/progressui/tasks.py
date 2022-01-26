from .backend import ProgressSend
from celery import shared_task
import time

@shared_task(bind=True)
def progress_test_task(self):
    progress_send = ProgressSend(self)
    r = 0
    for i in range(10):
        r = r + i
        progress_send.send_progress(percentage=(i+1)*10 , description='test')
        time.sleep(1)
    
    return r