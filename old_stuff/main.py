from  old_stuff.get_actual_pdf import *
from old_stuff.actual_pdf_to_csv import *


def main(base_url='http://www.fenabrave.org.br',dir_path="./relatorios_emplacamentos"):
    get_pdf_file(base_url)
    create_csv(dir_path)


if __name__ == '__main__':
    main()