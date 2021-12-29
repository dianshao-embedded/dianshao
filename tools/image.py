import os
from . import shell

# TODO: build image working on nand and nor

class ImageBuilder():

    def __init__(self, project_path, project_name):
        self.project = os.path.join(project_path, project_name)

    def create_image(self):
        pass