from  get_actual_pdf import *
from actual_pdf_to_csv import *


def main(base_url='http://www.fenabrave.org.br'):
    get_pdf_file(base_url)
    read_pdf(base_url)
    etl_pdf(base_url)
    create_csv(base_url)

if __name__ == '__main__':
    main()