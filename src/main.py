# import csv
import json
import os

from endpoints.endpoints import ConsultarTabelaDeReferencia, ConsultarAnoModeloPeloCodigoFipe, ConsultarValorComTodosParametros
from extractions.fipe_code_data import FipeCode

def main():
    base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
    fipe = FipeCode()
    fipe.url_base = base_url
    fipe.headers = headers
    fipe_code_list = fipe.get_soup_data()

    if not os.path.exists("./data/fipe_codes.json"):
        with open('./data/fipe_codes.json', 'w') as f:
            if fipe_code_list:  # Check if the list is not empty
                json.dump(fipe_code_list, f, indent=0)

    # if not os.path.exists("./data/fipe_codes.csv"):
    #     with open('./data/fipe_codes.csv', 'w', newline='') as f:
    #         if fipe_code_list:  # Check if the list is not empty
    #             fieldnames = fipe_code_list[0].keys()
    #             writer = csv.DictWriter(f, fieldnames=fieldnames)
    #             writer.writeheader()
    #             writer.writerows(fipe_code_list)

    data = ConsultarTabelaDeReferencia()
    data.endpoint_url = "ConsultarTabelaDeReferencia"
    codigo_tabela_referencia = data.get_endpoint_data()

    results = []
    final_data_list = []

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
                results.append(item)
                print(item)

                with open('./data/ano_combustivel.json', 'w') as jsonfile:
                    json.dump(results, jsonfile, indent=1)

            # Write the data to a CSV file
                # with open('./data/ano_combustivel.csv', 'w', newline='') as csvfile:
                #     fieldnames = results[0].keys()
                #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                #     writer.writeheader()
                #     for row in results:
                #         writer.writerow(row)

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
        print(final_data)

        with open('./data/fipe_car_data.json', 'w') as jsonfile:
            json.dump(final_data_list, jsonfile, indent=0)


    # Write the data to a CSV file
        # with open('./data/fipe_car_data.csv', 'w', newline='') as csvfile:
        #     fieldnames = final_data_list[0].keys()
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for row in final_data_list:
        #         writer.writerow(row)

if __name__ == "__main__":
    main()
