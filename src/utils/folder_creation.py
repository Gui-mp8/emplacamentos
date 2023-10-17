import os
from datetime import datetime
import json
from typing import List, Dict, Any

def folder_creation(json_data: List[Dict[str, Any]], file_name: str) -> None:
    # Get the current year and month
    now = datetime.now()
    year = now.year
    month = now.strftime('%m')

    # Create the "data" folder if it doesn't exist
    data_folder = './data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Create the year-month folder inside the "data" folder
    year_month_folder = os.path.join(data_folder, f'{year}-{month}')
    if not os.path.exists(year_month_folder):
        os.makedirs(year_month_folder)

    json_file_path = os.path.join(year_month_folder, f'{file_name}.json')

    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)