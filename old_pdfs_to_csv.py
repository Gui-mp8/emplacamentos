import PyPDF2
import csv
import os
import pandas as pd


def file_name():
    directory_path = "./relatorios_antigos"
    pdf_files = [file for file in os.listdir(directory_path) if file.endswith(".pdf")]
    pdf_files.sort() # sort the list of PDF files alphabetically
    pdf_file_name = pdf_files[7]

    return pdf_file_name

def read_pdf():
    pdf_file = f"./relatorios_antigos/{file_name()}" 
    pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))

    print('PDF lido!!!\n')
    return pdf_reader

page7 = read_pdf().pages[6]
text = page7.extract_text()

# Split the text into lines
lines = text.split("\n")

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

# Convert the list into a DataFrame
df = pd.DataFrame(list_output)
df = df[8:]

# set the column names attribute to a list of header names
df.columns = ['marca/modelo', 'qtd_emplacados']

# Eliminating the '.' in the string
df['qtd_emplacados'] = df['qtd_emplacados'].str.replace('.','')

# drop rows with null values
df = df.dropna()

# Reseting the index to eliminate any future problems.
df = df.reset_index(drop=True)

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
df['ano_mes'] = file_name()[:-6].replace('_','-') + '-01'

# Changing to int type
df['qtd_emplacados'] = df['qtd_emplacados'].astype(int)

# Find the index where the value jumps up
idx = df['qtd_emplacados'].idxmax()

# Split the dataframe into two at that index
df_automoveis = df.iloc[:idx]
df_comerciais_leves = df.iloc[idx:]

# Generating the csv's 
automoveis_csv = df_automoveis.to_csv(f'./automoveis/automoveis_{file_name()}.csv',sep=',',index=False,encoding='utf8')

comerciais_leves_csv = df_comerciais_leves.to_csv(f'./comerciais_leves/comerciais_leves_{file_name()}.csv',sep=',',index=False,encoding='utf8')


