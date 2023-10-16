import PyPDF2 
import csv
import os
import pandas as pd
from old_stuff.get_actual_pdf import *

def file_name(dir_path):
    pdf_files = [file for file in os.listdir(dir_path) if file.endswith(".pdf")]
    files = sorted(pdf_files, key=lambda x: os.path.getmtime(os.path.join(dir_path, x)), reverse=True)    
    pdf_file_name = files[0]
    return pdf_file_name.replace('.pdf','')

def extract_text_pdf(dir_path):
    pdf_file = f"./relatorios_emplacamentos/{file_name(dir_path)}.pdf" 
    pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))
    
    page7 = pdf_reader.pages[6]
    text = page7.extract_text()
    return text

def text_to_list(dir_path):

    # Split the text into lines
    lines7 = extract_text_pdf(dir_path).split("\n")

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

    return list_output

def list_to_df_etl(dir_path):

    df = pd.DataFrame(text_to_list(dir_path))
    df = df[8:]

    df = df.dropna()
    # Reseting the index to eliminate any future problems.
    df = df.reset_index(drop=True)

    # set the column names attribute to a list of header names
    df.columns = ['marca/modelo', 'qtd_emplacados']

    # Eliminating the '.' in the string
    df['qtd_emplacados'] = df['qtd_emplacados'].str.replace('.', '', regex=False)

    # Split the column into three columns
    df[['marca', 'modelo1', 'modelo2']] = df['marca/modelo'].str.split('/', expand=True)

    # Join the second and third columns back together with a '/'
    df['modelo'] = df[['modelo1', 'modelo2']].apply(lambda x: '/'.join(x.dropna().astype(str)), axis=1)

    # Drop the intermediate columns
    df = df.drop(columns=['marca/modelo', 'modelo1', 'modelo2'])

    # Correcting the last '/' from VW MAN/EXPRESS
    df['modelo'] = df['modelo'].apply(lambda x: '-'.join(x.rsplit('/', 1))) # rsplit splits x on the last occurrence of '/' and returns a list of two strings and join() joins the list of two strings with '-'.

    # Organazing the columns
    df = df[['marca','modelo','qtd_emplacados']]

    # Adding year_month column
    df['ano_mes'] = file_name(dir_path)[:-2].replace('_','-') + '-01'

    # Changing to int type
    df['qtd_emplacados'] = df['qtd_emplacados'].astype(int)

    return df

def create_csv(dir_path):

    df = list_to_df_etl(dir_path)
    # Find the index where the value jumps up
    idx = (df['qtd_emplacados'].diff()>0).idxmax()

    # Split the dataframe into two at those index values
    df_automoveis = df.iloc[:idx]
    df_automoveis['tipo'] = 'automoveis'
    df_automoveis.to_csv(f'./automoveis/automoveis_{file_name(dir_path)}.csv',sep=',',index=False,encoding='utf8')
    print(df_automoveis)
    print('-----------------------------------------------------')
    df_comerciais_leves = df.iloc[idx:]
    df_comerciais_leves['tipo'] = 'comerciais_leves'
    df_comerciais_leves.to_csv(f'./comerciais_leves/comerciais_leves_{file_name(dir_path)}.csv',sep=',',index=False,encoding='utf8')
    print(df_comerciais_leves)

    return print('Csvs criados')

dir_path="./relatorios_emplacamentos"
create_csv(dir_path)
