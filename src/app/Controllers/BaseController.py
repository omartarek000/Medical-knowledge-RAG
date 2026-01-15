from src.app.helpers.config import Settings , get_settings
import os
import string
import random


class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        # this get the root directory of the project
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.file_dir = os.path.join(project_root, self.app_settings.PROJECTS_DIR)
        
        
    def generate_random_string(self , length : int = 10):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))