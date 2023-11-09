import os
import json

class Validation():
    def check_folders(self, folder_path: str) -> bool:
        if os.path.exists(folder_path):
            return True
        return False

    def check_files(self, file_path: str) -> bool:
        if os.path.exists(file_path):
            data = json.load(file_path)
            if len(data) > 27000:
                return True
        return False