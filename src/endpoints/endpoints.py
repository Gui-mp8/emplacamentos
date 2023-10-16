from abc import ABC, abstractmethod
from typing import List, Dict, Any

import requests

class Endpoint(ABC):
    def __init__(self) -> None:
        self._endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/"
        # self._payload = kwargs.get('payload', {})

    @property
    def endpoint_url(self) -> str:
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, endpoint):
        self._endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/" + endpoint

    # @property
    # def payload(self) -> dict:
    #     return self._payload

    # @payload.setter
    # def payload(self, payload):
    #     self._payload = payload

    @abstractmethod
    def get_endpoint_response(self) -> requests.Response:
        pass

    @abstractmethod
    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        pass

class ConsultarTabelaDeReferencia(Endpoint):

    def get_endpoint_response(self) -> requests.Response:
        response = requests.post(self.endpoint_url)
        return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        return self.get_endpoint_response().json()

class ConsultarAnoModeloPeloCodigoFipe(Endpoint):
    def __init__(self, codigotabelareferencia: str, codigo_fipe: str) -> None:
        self.codigotabelareferencia = codigotabelareferencia
        self.codigo_fipe = codigo_fipe

    def get_endpoint_response(self) -> requests.Response:
        payload = {
            'codigoTipoVeiculo': '1',
            'codigoTabelaReferencia': f'{self.codigotabelareferencia}',
            'codigoModelo': '',
            'codigoMarca': '',
            'ano': '',
            'codigoTipoCombustivel': '',
            'anoModelo': '',
            'tipoVeiculo': '',
            'modeloCodigoExterno': f'{self.codigo_fipe}',
        }

        response = requests.post(self.endpoint_url,data=payload)
        return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        return self.get_endpoint_response().json()

if __name__ == "__main__":
    data = ConsultarTabelaDeReferencia()
    data.endpoint_url =  "ConsultarTabelaDeReferencia"
    print(data.get_endpoint_data()[0]["Codigo"])
