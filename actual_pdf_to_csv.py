import PyPDF2
import csv
import os
import pandas as pd
from get_actual_pdf import *


def read_pdf(base_url):

    pdf_file = f"./relatorios_emplacamento/{get_pdf_date(base_url)}.pdf" 
    pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))
    return pdf_reader

def etl_pdf(base_url):
    page7 = read_pdf(base_url).pages[6]  # 0-based index for page number

    text7 = page7.extract_text()

    # Split the text into lines
    lines7 = text7.split("\n")

    # Remove empty lines
    lines = [line for line in lines7 if line.strip()]

    # Convert the lines into a list
    list_output = [line.split() for line in lines]

    # Remove the first column from the list
    for i in range(len(list_output)):
        list_output[i] = list_output[i][1:]

    for row in list_output:
        if len(row) == 3:
            row[0] = row[0] + '-' + row[1]
            row.pop(1)
        elif len(row) == 4:
            row[0] = row[0] + '-' + row[1] + '-' + row[2]
            row.pop(1)
            row.pop(1)
        elif len(row) == 5:
            row[0] = row[0] + '-' + row[1] + '-' + row[2] + '-' + row[3]
            row.pop(1)
            row.pop(1)
            row.pop(1)

 # Replace forward slashes with commas in each row
    for row in list_output:
        for i in range(len(row)):
            split_values = row[i].split('/')
            if len(split_values) == 2:
                row[i] = split_values[0]
                row.insert(i+1, split_values[1])
    

    # Add headers to the list
    list_output.insert(0, ['marca', 'modelo', 'qtd_emplacados'])

    # Remove empty row
    list_output.pop(1)

# Replacing the dots with empty spaces cause the data type should be int and not float
    for row in list_output:
        for i in range(len(row)):
            row[i] = row[i].replace('.','') # assign the result of replace() back to row[i]

    return list_output

def create_csv(base_url):

        # Create directories for CSV files
    if not os.path.exists('automoveis'):
        os.mkdir('automoveis')

    if not os.path.exists('comerciais_leves'):
        os.mkdir('comerciais_leves')

    ano_mes = get_pdf_date(base_url)

    # Write the list to a CSV file with headers
    with open(f'automoveis/automoveis_{ano_mes}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(etl_pdf(base_url)[0])
        writer.writerows(etl_pdf(base_url)[8:58])

    with open(f'comerciais_leves/comerciais_leves_{ano_mes}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(etl_pdf(base_url)[0])
        writer.writerows(etl_pdf(base_url)[61:])

def etl_csv(base_url):

    ano_mes = get_pdf_date(base_url)

    df_automoveis = pd.read_csv(f'./automoveis/automoveis_{ano_mes}.csv')
    df_automoveis['qtd_emplacados'] = df_automoveis['qtd_emplacados'].astype(float)
    df_automoveis['ano_mes'] = ano_mes[:-2].replace('_','-')
    changed_csv_automoveis = df_automoveis.to_csv(f'./automoveis/automoveis_{ano_mes}.csv',sep=',',index=False,encoding='utf8')

    df_comerciais_leves = pd.read_csv(f'./comerciais_leves/comerciais_leves_{ano_mes}.csv')
    df_comerciais_leves['ano_mes'] = ano_mes[:-2].replace('_','-')
    changed_csv_comerciais_leves = df_comerciais_leves.to_csv(f'./comerciais_leves/comerciais_leves_{ano_mes}.csv',sep=',',index=False,encoding='utf8')

    return changed_csv_automoveis,changed_csv_comerciais_leves

