import csv

from endpoints.endpoints import ConsultarTabelaDeReferencia, ConsultarAnoModeloPeloCodigoFipe, ConsultarValorComTodosParametros
from fipe_code_extraction.response_fipe_code import FipeCode

def main():
    data = ConsultarTabelaDeReferencia()
    data.endpoint_url = "ConsultarTabelaDeReferencia"
    codigo_tabela_referencia = data.get_endpoint_data()

    base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
    fipe = FipeCode()
    fipe.url_base = base_url
    fipe.headers = headers
    fipe_code_list = fipe.get_soup_data()

    results = []
    final_data_list = []

    for codigo_fipe in fipe_code_list:
        data = ConsultarAnoModeloPeloCodigoFipe(
            codigo_tabela_referencia=codigo_tabela_referencia[0]["Codigo"],
            codigo_fipe=codigo_fipe["code"]
        )
        data.endpoint_url = "ConsultarAnoModeloPeloCodigoFipe"
        response_data = data.get_endpoint_data()

        for item in response_data:
            item["codigo_tabela_referencia"] = codigo_tabela_referencia[0]["Codigo"]
            item["codigo_fipe"] = codigo_fipe["code"]
            item["ano_modelo"] = item["Value"].split("-")[0]
            item["codigo_tipo_combustivel"] = item["Value"].split("-")[1]
            results.append(item)
            print(item)

        # Write the data to a CSV file
            with open('results.csv', 'w', newline='') as csvfile:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in results:
                    writer.writerow(row)

    for values in results:
        data = ConsultarValorComTodosParametros(
            codigo_tabela_referencia=values["codigo_tabela_referencia"],
            codigo_fipe=values["codigo_fipe"],
            ano_modelo=values["ano_modelo"],
            codigo_tipo_combustivel=values["codigo_tipo_combustivel"]
        )
        data.endpoint_url = "ConsultarValorComTodosParametros"
        final_data = data.get_endpoint_data()
        final_data_list.append(final_data)

    # Write the data to a CSV file
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = final_data_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in final_data_list:
            writer.writerow(row)

if __name__ == "__main__":
    main()
