from abc import ABC, abstractmethod
from typing import List, Dict, Any

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
    def create_session(self) -> requests.Session:
        pass

    @abstractmethod
    def get_endpoint_response(self) -> requests.Response:
        pass

    @abstractmethod
    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        pass

class ConsultarTabelaDeReferencia(Endpoint):
    def create_session(self):
        session = None

        if session is None:
            session = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=2,
                            status_forcelist=[500, 502, 503, 504, 520])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

        return session

    def get_endpoint_response(self) -> requests.Response:
        response = self.create_session().post(self.endpoint_url)
        if response.status_code == 520:
                print("Server Error (Status Code 520). Skipping this request.")
                return None
        else:
            return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        response = self.get_endpoint_response()

        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Request failed with status code {response.status_code}")

        try:
            data = response.json()
            return data
        except ValueError:
            raise requests.exceptions.JSONDecodeError("Failed to decode response as JSON", response.text, 0)

class ConsultarAnoModeloPeloCodigoFipe(Endpoint):
    def __init__(self, **kwargs) -> None:
        self.codigo_tabela_referencia = kwargs.get("codigo_tabela_referencia")
        self.codigo_fipe = kwargs.get("codigo_fipe")

    def create_session(self):
        session = None

        if session is None:
            session = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=2,
                            status_forcelist=[500, 502, 503, 504, 520])
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

        # if response.status_code != 200:
        #     raise requests.exceptions.RequestException(f"Request failed with status code {response.status_code}")
        if response.content  == None:
            print(f"None data for the fipe code: {self.codigo_fipe}")
            pass

        try:
            data = response.json()
            return data
        except ValueError:
            raise requests.exceptions.JSONDecodeError("Failed to decode response as JSON", response.text, 0)


class ConsultarValorComTodosParametros(Endpoint):
    def __init__(self, **kwargs) -> None:
        self.codigo_tabela_referencia = kwargs.get("codigo_tabela_referencia")
        self.codigo_fipe = kwargs.get("codigo_fipe")
        self.ano_modelo = kwargs.get("ano_modelo")
        self.codigo_tipo_combustivel = kwargs.get("codigo_tipo_combustivel")

    def create_session(self):
        session = None

        if session is None:
            session = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=2,
                            status_forcelist=[500, 502, 503, 504, 520])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

        return session

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

        response = self.create_session().post(self.endpoint_url,data=payload)
        if response.status_code == 520:
                print("Server Error (Status Code 520). Skipping this request.")
                return None
        else:
            return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        response = self.get_endpoint_response()

        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Request failed with status code {response.status_code}")

        try:
            data = response.json()
            return data
        except ValueError:
            raise requests.exceptions.JSONDecodeError("Failed to decode response as JSON", response.text, 0)


