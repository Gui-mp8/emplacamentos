import os
from datetime import datetime
import json
from typing import List, Dict, Any

from abstractions.saving_files_abstraction import SavingFiles

class JsonFiles(SavingFiles):
    def __init__(self) -> None:
        self.principal_folder = './data'
        self.date = datetime.now().strftime("%Y-%m")

    def folder_creation(self) -> None:
        if not os.path.exists(self.principal_folder):
            os.makedirs(self.principal_folder)
            print(f'{self.principal_folder} folder created!!!')

        year_month_folder = os.path.join(self.principal_folder, f'{self.date}')
        if not os.path.exists(year_month_folder):
            os.makedirs(year_month_folder)
            print(f'{year_month_folder} folder created!!!')

    def writing_data(self, data: List[Dict[str, Any]], file_name: str) -> None:
        self.folder_creation()

        date_folder = os.path.join(self.principal_folder, f'{self.date}')
        json_file_path = os.path.join(date_folder, f'{file_name}_{self.date}.json')

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)