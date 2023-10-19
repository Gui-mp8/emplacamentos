import os

from extractions.fipe_code_data import FipeCode
from extractions.endpoints.tabela_referencia import ConsultarTabelaDeReferencia
from extractions.endpoints.ano_modelo_codigo_fipe import ConsultarAnoModeloPeloCodigoFipe
from extractions.endpoints.valor_todos_parametros import ConsultarValorComTodosParametros
from utils.saving_files import CsvFiles

def main():

    base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
    fipe = FipeCode()
    fipe.url_base = base_url
    fipe.headers = headers
    fipe_code_list = fipe.get_soup_data()

    CsvFiles().writing_data(fipe_code_list, "fipe_codes")

    data = ConsultarTabelaDeReferencia()
    data.endpoint_url = "ConsultarTabelaDeReferencia"
    codigo_tabela_referencia = data.get_endpoint_data()

    ano_combustivel = []
    fipe_car_data = []

    for codigo_fipe in fipe_code_list:
        data = ConsultarAnoModeloPeloCodigoFipe(
            codigo_tabela_referencia=codigo_tabela_referencia[0]["Codigo"],
            codigo_fipe=codigo_fipe["code"]
        )
        data.endpoint_url = "ConsultarAnoModeloPeloCodigoFipe"
        response_data = data.get_endpoint_data()

        if not response_data:
            print(f"No data for the fipe code: {codigo_fipe['code']}")

        else:
            for item in response_data:
                item["codigo_tabela_referencia"] = codigo_tabela_referencia[0]["Codigo"]
                item["codigo_fipe"] = codigo_fipe["code"]
                item["ano_modelo"] = item["Value"].split("-")[0]
                item["codigo_tipo_combustivel"] = item["Value"].split("-")[1]
                ano_combustivel.append(item)
                print(item)

                CsvFiles().writing_data(ano_combustivel, "ano_combustivel")

    for values in ano_combustivel:
        data = ConsultarValorComTodosParametros(
            codigo_tabela_referencia=values["codigo_tabela_referencia"],
            codigo_fipe=values["codigo_fipe"],
            ano_modelo=values["ano_modelo"],
            codigo_tipo_combustivel=values["codigo_tipo_combustivel"]
        )
        data.endpoint_url = "ConsultarValorComTodosParametros"
        final_data = data.get_endpoint_data()
        fipe_car_data.append(final_data)
        print(final_data)

        CsvFiles().writing_data(fipe_car_data, "fipe_car_data")

if __name__ == "__main__":
    main()
