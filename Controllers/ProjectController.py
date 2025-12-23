from .BaseController import basecontroller
from fastapi import UploadFile
from Models import ResponseSignal
import os

class projectcontroller (basecontroller) :

    def __init__(self):
        super().__init__()

    def get_project_path (self,project_id : str) :
            
            project_path = os.path.join(self.files_dir, project_id)
            
            if not os.path.exists(project_path)  :
                os.makedirs(project_path)

            return project_path