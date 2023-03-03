import requests
import os
from bs4 import BeautifulSoup


def get_pdf_date(base_url):
    '''This function gets the date that's
    necessary to get the right pdfs'''
    
    # Make a request to the webpage and get the HTML content
    url = f"{base_url}/portalv2/Conteudo/Emplacamentos"
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the links on the page that point to PDF files
    links = soup.find_all("a", href=True, string="Download")

    # Loop through the links and extract the date string from each PDF URL
    dates = []
    for link in links:
        pdf_url = link["href"]
        date_str = pdf_url.split("/")[-1].split(".")[0]
        date = date_str.split("_")[0] + '_' + date_str.split("_")[1] + '_' + date_str.split("_")[2]
        dates.append(date)

    # Print the list of date strings
    current_year_month = dates[0]

    return current_year_month

# getting the pdfs from every month starting from 2023_01
def get_pdf_file(base_url):
    # Create the directory for storing the PDFs
    if not os.path.exists('relatorios_emplacamento'):
        os.makedirs('relatorios_emplacamento')

    pdf_url = f"{base_url}/portal/files/{get_pdf_date(base_url)}.pdf"

    # Send a GET request to the URL of the PDF file
    response = requests.get(pdf_url)

    # Save the PDF contents to a file in the 'relatorios' directory
    filename = os.path.join('relatorios_emplacamento', f"{get_pdf_date(base_url)}.pdf")
    with open(filename, 'wb') as f:
        f.write(response.content)
        print(f"Downloaded {filename}")
