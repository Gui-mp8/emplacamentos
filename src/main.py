from endpoints.endpoints import ConsultarTabelaDeReferencia, ConsultarAnoModeloPeloCodigoFipe
from fipe_code_extraction.response_fipe_code import FipeCode

def main():
    data = ConsultarTabelaDeReferencia()
    data.endpoint_url =  "ConsultarTabelaDeReferencia"
    codigotabelareferencia = data.get_endpoint_data()

    base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
    headers = {"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
    fipe = FipeCode()
    fipe.url_base = base_url
    fipe.headers = headers
    fipe_code_list = fipe.get_soup_data()

    results = []

    for codigo_fipe in fipe_code_list:
        data = ConsultarAnoModeloPeloCodigoFipe(
            codigotabelareferencia=codigotabelareferencia[0]["Codigo"],
            codigo_fipe=codigo_fipe["code"]
        )
        data.endpoint_url = "ConsultarAnoModeloPeloCodigoFipe"
        response_data = data.get_endpoint_data()

        for item in response_data:
            item["codigo_fipe"] = codigo_fipe["code"]
            item["Value"] = item["Value"][:4]
            results.append(item)
            print(results)

    # Now, 'results' contains the data with the "codigo_fipe" included
    print(results)

if __name__ == "__main__":
    main()