import pandas as pd
import time  # Import the time module

from extractions.fipe_code_data import FipeCode
from extractions.endpoints.tabela_referencia import ConsultarTabelaDeReferencia
from extractions.endpoints.ano_modelo_codigo_fipe import ConsultarAnoModeloPeloCodigoFipe
from extractions.endpoints.valor_todos_parametros import ConsultarValorComTodosParametros
from utils.saving_files import JsonFiles, CsvFiles
from treatment.month_translation import month_translation

def main():
    start_time = time.time()  # Record the start time

    base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
    fipe = FipeCode()
    fipe.url_base = base_url
    fipe.headers = headers
    fipe_code_list = fipe.get_soup_data()
    JsonFiles().writing_data(fipe_code_list, "fipe_codes")

    data = ConsultarTabelaDeReferencia()
    data.endpoint_url = "ConsultarTabelaDeReferencia"
    codigo_tabela_referencia = data.get_endpoint_data()
    JsonFiles().writing_data(codigo_tabela_referencia, "codigo_tabela_referencia")

    ano_combustivel = []
    for codigo_fipe in fipe_code_list:
        data = ConsultarAnoModeloPeloCodigoFipe(
            codigo_tabela_referencia=codigo_tabela_referencia[0]["Codigo"],
            codigo_fipe=codigo_fipe["code"],
            mes_referencia=month_translation(codigo_tabela_referencia[0]["Mes"])
        )
        data.endpoint_url = "ConsultarAnoModeloPeloCodigoFipe"
        response_data = data.get_endpoint_data()
        for item in response_data:
            ano_combustivel.append(item)
            JsonFiles().writing_data(ano_combustivel, "ano_combustivel")

    df = pd.read_json("/home/guilherme/Documentos/vscode/projetos/emplacamentos/data/2023-10/ano_combustivel_2023-10.json")
    print(df.to_string())
    fipe_car_data = []

    for index, row in df.iterrows():
        data = ConsultarValorComTodosParametros(
            codigo_tabela_referencia=row["codigo_tabela_referencia"],
            codigo_fipe=row["codigo_fipe"],
            ano_modelo=row["ano_modelo"],
            codigo_tipo_combustivel=row["codigo_tipo_combustivel"],
            mes_referencia=row["mes_referencia"]
        )
        data.endpoint_url = "ConsultarValorComTodosParametros"
        final_data = data.get_endpoint_data()

        fipe_car_data.append(final_data)
        print(final_data)

        CsvFiles().writing_data(fipe_car_data, "fipe_car_data")

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Program execution time: {elapsed_time} seconds")

if __name__ == "__main__":
    main()
