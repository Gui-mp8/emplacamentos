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
    def __init__(self, **kwargs) -> None:
        self.codigo_tabela_referencia = kwargs.get("codigo_tabela_referencia")
        self.codigo_fipe = kwargs.get("codigo_fipe")

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

        response = requests.post(self.endpoint_url,data=payload)
        return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        return self.get_endpoint_response().json()

class ConsultarValorComTodosParametros(Endpoint):
    def __init__(self, **kwargs) -> None:
        self.codigo_tabela_referencia = kwargs.get("codigo_tabela_referencia")
        self.codigo_fipe = kwargs.get("codigo_fipe")
        self.ano_modelo = kwargs.get("ano_modelo")
        self.codigo_tipo_combustivel = kwargs.get("codigo_tipo_combustivel")

    def get_endpoint_response(self) -> requests.Response:
        payload = {
            'codigoTabelaReferencia': f'{self.codigo_tabela_referencia}',
            'codigoMarca': '',
            'codigoModelo': '',
            'codigoTipoVeiculo': '1',
            'anoModelo': f'{self.ano_modelo}',
            'codigoTipoCombustivel': f'{self.codigo_tipo_combustivel}',
            'tipoVeiculo': 'carro',
            'modeloCodigoExterno': f'{self.codigo_fipe}',
            'tipoConsulta': 'codigo'
        }

        response = requests.post(self.endpoint_url,data=payload)
        return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        return self.get_endpoint_response().json()

# if __name__ == "__main__":
#     data = ConsultarTabelaDeReferencia()
#     data.endpoint_url =  "ConsultarTabelaDeReferencia"
#     print(data.get_endpoint_data()[0]["Codigo"])
