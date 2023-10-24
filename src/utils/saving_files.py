import os
from datetime import datetime
import csv
import json
from typing import List, Dict, Any

from abstractions.saving_files_abstraction import SavingFiles
from utils.checking_files import Validation

class JsonFiles(SavingFiles):
    def __init__(self) -> None:
        self.principal_folder = './data'
        self.date = datetime.now().strftime("%Y-%m")

    def folder_creation(self) -> None:
        if Validation.check_folders(self.principal_folder) == False:
            os.makedirs(self.principal_folder)
            print(f'{self.principal_folder} folder created!!!')

        files_folder = os.path.join(self.principal_folder, f'{self.date}')
        if Validation.check_folders(files_folder) == False:
            os.makedirs(files_folder)
            print(f'{files_folder} folder created!!!')

    def writing_data(self, data: List[Dict[str, Any]], file_name: str) -> None:
        self.folder_creation()

        date_folder = os.path.join(self.principal_folder, f'{self.date}')
        json_file_path = os.path.join(date_folder, f'{file_name}_{self.date}.json')

        # if Validation().checking_csv_data(file_path=csv_file_path, file_name=file_name) == False:
        if data != {}:
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4, default=str)

class CsvFiles(SavingFiles):
    def __init__(self) -> None:
        self.principal_folder = './data'
        self.date = datetime.now().strftime("%Y-%m")

    def folder_creation(self) -> None:
        if Validation().check_folders(self.principal_folder) == False:
            os.makedirs(self.principal_folder)
            print(f'{self.principal_folder} folder created!!!')

        files_folder = os.path.join(self.principal_folder, f'{self.date}')
        if Validation().check_folders(files_folder) == False:
            os.makedirs(files_folder)
            print(f'{files_folder} folder created!!!')

    def writing_data(self, data: List[Dict[str, Any]], file_name: str) -> None:
        self.folder_creation()

        date_folder = os.path.join(self.principal_folder, f'{self.date}')
        csv_file_path = os.path.join(date_folder, f'{file_name}_{self.date}.csv')

        if data != {}:
            with open(csv_file_path, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)