import os

class Validation():
    def check_folders(self, folder_path: str) -> bool:
        if os.path.exists(folder_path):
            return True
        return False
