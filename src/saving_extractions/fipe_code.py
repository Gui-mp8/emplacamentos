import csv

from extractions_data.fipe_code_data import FipeCode

def get_fipe_code_csv():
    base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
    fipe = FipeCode()
    fipe.url_base = base_url
    fipe.headers = headers
    fipe_code_list = fipe.get_soup_data()

    with open('./data/fipe_codes.csv', 'w', newline='') as f:
        if fipe_code_list:  # Check if the list is not empty
            fieldnames = fipe_code_list[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(fipe_code_list)

