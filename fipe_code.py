import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json
import time
import os
from datetime import datetime, timedelta

def get_fipe_codes():
    url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    fipe_codes = []
    for tag in soup.select('a[title^="Tabela FIPE código"]'):
        codigo_fipe = tag['href'][-8:]
        fipe_codes.append(codigo_fipe)

    return fipe_codes

def get_csv():
    with open('codigos_fipe.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['codigo_fipe'])
        writer.writerows(zip(get_fipe_codes()))

# Create a new JSON file with a unique filename each day
today = datetime.today().strftime('%Y-%m-%d')
filename = f'json_data_{today}.json'

if os.path.exists(f'{filename}'):
    # If the file already exists, read its contents into json_data
    with open(filename, 'r', encoding='utf-8') as infile:
        json_data = json.load(infile)
else:
    # If the file doesn't exist, create an empty json_data list
    json_data = []

n = len(json_data)

for code in get_fipe_codes()[n:]:
    url_api = f'https://brasilapi.com.br/api/fipe/preco/v1/{code}'
    response = requests.get(url_api)
    api_json = response.text
    json_data.append(json.loads(api_json))
    n += 1
    print(f'{n}/{len(get_fipe_codes())}')
    time.sleep(7)

# Write the updated json_data to the file
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False)
        print(f'json {n} salvo!!')
