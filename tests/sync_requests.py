import pandas as pd
import requests

df = pd.read_json("./data/2023-10/fipe_codes_2023-10.json")
data = []
for index, row in df.iterrows():
    print(f"Working on fipe code: {row.iloc[0]}")
    payload = {
        'codigoTipoVeiculo': '1',
        'codigoTabelaReferencia': '302',
        'codigoModelo': '',
        'codigoMarca': '',
        'ano': '',
        'codigoTipoCombustivel': '',
        'anoModelo': '',
        'tipoVeiculo': '',
        'modeloCodigoExterno': f'{row.iloc[0]}',
    }

    url = "https://veiculos.fipe.org.br/api/veiculos/ConsultarAnoModeloPeloCodigoFipe"
    response = requests.post(url,data=payload)

    data.append(response.json())
    # print(data)

