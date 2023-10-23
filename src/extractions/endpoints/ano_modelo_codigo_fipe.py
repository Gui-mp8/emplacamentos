from typing import List, Dict, Any
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from abstractions.endpoints_abstraction import Endpoint
from models.ano_modelo import AnoModelo

class ConsultarAnoModeloPeloCodigoFipe(Endpoint):
    def __init__(self, **kwargs) -> None:
        self.codigo_tabela_referencia = kwargs.get("codigo_tabela_referencia")
        self.codigo_fipe = kwargs.get("codigo_fipe")
        self.mes_referencia = kwargs.get("mes_referencia")

    def create_session(self) -> requests.Session():
        session = None

        if session is None:
            session = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=2,
                            status_forcelist=[500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

        return session

    def get_endpoint_response(self) -> requests.Response:
        payload = {
            'codigoTipoVeiculo': '1',
            'codigoTabelaReferencia': f'{self.codigo_tabela_referencia}',
            'codigoModelo': '',
            'codigoMarca': '',
            'ano': '',
            'codigoTipoCombustivel': '',
            'anoModelo': '',
            'tipoVeiculo': '',
            'modeloCodigoExterno': f'{self.codigo_fipe}',
        }

        response = self.create_session().post(self.endpoint_url,data=payload)
        if response.status_code == 520:
                print("Server Error (Status Code 520). Skipping this request.")
                return None
        else:
            return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        response = self.get_endpoint_response()

        if response is None:
            # Skip this request and return an empty list or handle it as needed
            print(f"None data for the fipe code: {self.codigo_fipe}")
            return None

        try:
            data = response.json()
            carros = []
            for index, item in enumerate(data, start=1):
                carro = AnoModelo(
                    ano_modelo=item["Value"].split("-")[0],
                    codigo_tipo_combustivel=item["Value"].split("-")[1],
                    codigo_tabela_referencia=self.codigo_tabela_referencia,
                    codigo_fipe=self.codigo_fipe,
                    mes_referencia=self.mes_referencia,
                    extraction_date=datetime.now().strftime("%Y-%m-%d")
                )
                carros.append(carro.model_dump())
                print(carro)

            return carros

        except ValueError:
            print(requests.exceptions.JSONDecodeError("Failed to decode response as JSON", response.text, 0))
            return {}

