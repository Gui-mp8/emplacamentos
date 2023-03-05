import PyPDF2
import csv
import os
import pandas as pd


directory_path = "./relatorios_antigos"
pdf_files = [file for file in os.listdir(directory_path) if file.endswith(".pdf")]
pdf_files.sort() # sort the list of PDF files alphabetically
pdf_file_name = pdf_files[1]

print(f'O pdf {pdf_file_name} sera lido e tratado')

pdf_file = f"./relatorios_antigos/{pdf_file_name}" 
pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))
pdf_file_name = pdf_file_name.replace('.pdf','')
print('\nPDF lido!!!')

page7 = pdf_reader.pages[6]
text = page7.extract_text()

print(f'Texto extraido: \n{text}')
# Split the text into lines
lines = text.split("\n")

# Convert the lines into a list
list_output = [line.split() for line in lines]

# Remove the first column from the list
for i in range(len(list_output)):
    list_output[i] = list_output[i][1:]

print(f'Lista antes do ultimo tratamento: \n{list_output}')

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


print(f'Lista final: \n{list_output}')

# Convert the list into a DataFrame
df = pd.DataFrame(list_output)
df = df[8:]

# drop rows with null values
df = df.dropna()

# Reseting the index to eliminate any future problems.
df = df.reset_index(drop=True)

# set the column names attribute to a list of header names
df.columns = ['marca/modelo', 'qtd_emplacados']

print(f'Dataframe criado para mais tratamentos: \n{df.to_string()}')

# Eliminating the '.' in the string
df['qtd_emplacados'] = df['qtd_emplacados'].str.replace('.', '', regex=False)

print(df.to_string())

# Split the column into three columns
df[['marca', 'modelo1', 'modelo2']] = df['marca/modelo'].str.split('/', expand=True)

print(df.to_string())

# Join the second and third columns back together with a '/'
df['modelo'] = df[['modelo1', 'modelo2']].apply(lambda x: '/'.join(x.dropna().astype(str)), axis=1)

print(df.to_string())

# Drop the intermediate columns
df = df.drop(columns=['marca/modelo', 'modelo1', 'modelo2'])

print(df.to_string())

# Correcting the last '/' from VW MAN/EXPRESS
df['modelo'] = df['modelo'].apply(lambda x: '-'.join(x.rsplit('/', 1))) # rsplit splits x on the last occurrence of '/' and returns a list of two strings and join() joins the list of two strings with '-'.
print(df.to_string())

# Organazing the columns
df = df[['marca','modelo','qtd_emplacados']]

# Adding year_month column
df['ano_mes'] = pdf_file_name[:-2].replace('_','-') + '-01'

print(df.to_string())

# Changing to int type
df['qtd_emplacados'] = df['qtd_emplacados'].astype(int)

# Find the index where the value jumps up
idx = df[(df.index >= 40) & (df.index <= 51) & (df['qtd_emplacados'] > 30000)].index

print(idx)

# Split the dataframe into two at those index values
if len(idx) > 0:
    split_index = idx[0]
    df_automoveis = df.loc[:split_index-1]
    automoveis_csv = df_automoveis.to_csv(f'./automoveis/automoveis_{pdf_file_name}.csv',sep=',',index=False,encoding='utf8')
    print(df_automoveis)
    print('-----------------------------------------------------')
    df_comerciais_leves = df.loc[split_index:]
    comerciais_leves_csv = df_comerciais_leves.to_csv(f'./comerciais_leves/comerciais_leves_{pdf_file_name}.csv',sep=',',index=False,encoding='utf8')
    print(df_comerciais_leves)
else:
    df_1 = df
    df_2 = None

# # Split the dataframe into two at that index
# df_automoveis = df.iloc[:idx]
# print(f'Automoveis: \n{df_automoveis.to_string()}')

# df_comerciais_leves = df.iloc[idx:]
# #print(f'Comerciais_leves: \n{df_comerciais_leves.to_string()}')

# # Generating the csv's 
# automoveis_csv = df_automoveis.to_csv(f'./automoveis/automoveis_{pdf_file_name}.csv',sep=',',index=False,encoding='utf8')

# comerciais_leves_csv = df_comerciais_leves.to_csv(f'./comerciais_leves/comerciais_leves_{pdf_file_name}.csv',sep=',',index=False,encoding='utf8')

# print("csv's gerados!")
