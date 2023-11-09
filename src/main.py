import os
import time  # Import the time module
from datetime import datetime

import pandas as pd
import asyncio

from utils.config import load_config
from etl.extractions.scraper.fipe_code_data import FipeCode
from etl.extractions.endpoints.tabela_referencia import ConsultarTabelaDeReferencia
from etl.extractions.endpoints.ano_modelo_codigo_fipe import ConsultarAnoModeloPeloCodigoFipe
from etl.extractions.endpoints.valor_todos_parametros import ConsultarValorComTodosParametros
from utils.saving_files import JsonFiles, CsvFiles
from etl.treatment.month_translation import month_translation
from etl.load.dw.bigquery.dataset import BigQueryDataset
from etl.load.dw.bigquery.table import BigQueryTable

def main(config):
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
    # JsonFiles().writing_data(codigo_tabela_referencia, "codigo_tabela_referencia")

    # ano_combustivel = []
    # for codigo_fipe in fipe_code_list:
    #     data = ConsultarAnoModeloPeloCodigoFipe(
    #         codigo_tabela_referencia=codigo_tabela_referencia[0]["Codigo"],
    #         codigo_fipe=codigo_fipe["code"],
    #         mes_referencia=month_translation(codigo_tabela_referencia[0]["Mes"])
    #     )
    #     data.endpoint_url = "ConsultarAnoModeloPeloCodigoFipe"
    #     response_data = data.get_endpoint_data()

    #     if response_data != {}:

    #         for item in response_data:
    #             ano_combustivel.append(item)
    #             JsonFiles().writing_data(ano_combustivel, "ano_combustivel")

    #     else:
    #         print("Empty Data, skipping this row")


    # df = pd.read_json(f"./data/{datetime.now().strftime('%Y-%m')}/fipe_car_data_{datetime.now().strftime('%Y-%m')}/ano_combustivel_{datetime.now().strftime('%Y-%m')}.json")

    endpoint = ConsultarValorComTodosParametros()
    endpoint.endpoint_url = "ConsultarValorComTodosParametros"
    endpoint.dataframe = pd.read_json(f"./data/{datetime.now().strftime('%Y-%m')}/ano_combustivel_{datetime.now().strftime('%Y-%m')}.json")

    fipe_car_data = asyncio.run(endpoint.get_endpoint_data())

    CsvFiles().writing_data(fipe_car_data, "fipe_car_data")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Program execution time: {elapsed_time} seconds")

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './src/utils/emplacamentos-analise.json'
    config = load_config()
    main(config)