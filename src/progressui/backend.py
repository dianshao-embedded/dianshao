class ProgressSend():

    def __init__(self, task):
        self.task = task
        self.description = ""
        self.percentage = 0
        self.subProgress = []
        self.header = ""
    
    def send_progress(self, percentage=None, subProgress=[], description="", header=""):
        state = 'PROGRESS'
        if percentage is None:
            percentage = self.percentage
        else:
            self.percentage = percentage

        if len(subProgress) == 0:
            subProgress = self.subProgress
        else:
            self.subProgress = subProgress

        if description == "":
            description = self.description
        else:
            self.description = description

        if header == "":
            header = self.header
        else:
            self.header = header

        meta = {
            'percentage': percentage,
            'description': description,
            'subProgress': subProgress,
            'header': header,
        }
        self.task.update_state(
            state=state,
            meta=meta,
        )

        return state, meta

# TODO: Add Failure message set

class ProgressReceive():
    
    def __init__(self, result):
        self.result = result

    def get_data(self):
        meta = self.result._get_task_meta()
        state = meta["status"]
        data = {}
        if state == 'PROGRESS':
            data = meta["result"]
            data.update({
                'state': state,
                'completed': False,
            })
        elif state == 'SUCCESS':
            data = {
                'state': state,
                'completed': True,
            }
        elif state == 'FAILURE':
            data = {
                'state': 'FAILURE',
                'completed': True,
            }
        
        return data