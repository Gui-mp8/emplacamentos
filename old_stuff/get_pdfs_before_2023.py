import requests
import os

# Define the base URL for the PDFs
base_url = 'http://www.fenabrave.org.br'

# getting the pdfs from 2010 to 2022
try:
    # Iterate over the years from 2010 to 2022
    for year in range(2015, 2022):
        # Construct the URL for the PDF for the current year
        pdf_url = f"{base_url}/portal/files/{year}_12_2.pdf"

        # Send a GET request to the URL of the PDF file
        response = requests.get(pdf_url)

        # Save the PDF contents to a file in the 'relatorios' directory
        filename = os.path.join('relatorios_emplacamento', f"{year}_12_2.pdf")
        with open(filename, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded {filename}")
except:
    pass



