
import requests
import os
from projects.models import MyImage

class DishesAgent():

    def __init__(self, image_id):
        self.image = MyImage.objects.get(id=image_id)

    def upload_package(self):
        file_path = os.path.join(self.image.project.project_path,
                    self.image.project.project_name, self.image.file_path)

        file = os.path.join(file_path, self.image.file_name)
        file_url = self.image.dishes_url + "/api/v1/firmwares/upload/" + self.image.product_id + "/" + self.image.stage + "/" + self.image.version
        resp = requests.post(file_url, files = {"file": open(file, 'rb')})
        if resp.status_code != 200:
            print(resp.text)
            raise Exception("file upload error")
        
        post_url = self.image.dishes_url + "/api/v1/firmwares"
        resp = requests.post(post_url, json={
            "name": self.image.file_name,
            "product_id": self.image.product_id,
            "size": str(os.path.getsize(file)),
            "stage": self.image.stage,
            "status": "pending",
            "version": self.image.version
        })
        if resp.status_code != 200:
            raise Exception("firmware create error")
        