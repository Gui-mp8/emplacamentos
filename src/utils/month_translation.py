from datetime import datetime

def month_translation(mes_string: str) -> str:
    month_translation = {
        'janeiro': '1',
        'fevereiro': '2',
        'março': '3',
        'abril': '4',
        'maio': '5',
        'junho': '6',
        'julho': '7',
        'agosto': '8',
        'setembro': '9',
        'outubro': '10',
        'novembro': '11',
        'dezembro': '12'
    }
    if "/" in mes_string:
        month = mes_string.split('/')[0]
        year = mes_string.split('/')[1]

    elif " " in mes_string:
        month = mes_string.split(" ")[0]
        year = mes_string.split(" ")[2]

    month_number = month_translation.get(month.lower(), month)
    mes_referencia = f"{year}-{month_number}-01"

    return mes_referencia
