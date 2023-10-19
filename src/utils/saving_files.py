import os
from datetime import datetime
import csv
from typing import List, Dict, Any

from abstractions.saving_files_abstraction import SavingFiles

class CsvFiles(SavingFiles):
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
        csv_file_path = os.path.join(date_folder, f'{file_name}_{self.date}.csv')

        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    # def check_existing_data(file_name: str):
    #     date_folder = os.path.join(self.principal_folder, f'{self.date}')
    #     json_file_path = os.path.join(date_folder, f'{file_name}_{self.date}.json')

    #     with open(f'{self.principal_folder}/fipe_codes_{self.date}', 'r') as f:
    #         total_codes = json.load(f)

    #     with open(json_file_path, "r") as f:
    #         executed_codes = json.load(f)

    #     remaining_codes = list(set(total_codes) - set(executed_codes))
    #     for fipe_code in remaining_codes:
    #         self.writing_data(data, file_name)