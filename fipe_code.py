import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.tabelafipebrasil.com/fipe/carros'
headers = {"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

fipe_code = []
for tag in soup.select('a[title^="Tabela FIPE código"]'):
    codigo_fipe = tag['href'][-8:]
    fipe_code.append(codigo_fipe)

with open('codigos_fipe.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo_fipe'])
    writer.writerows(zip(fipe_code))
