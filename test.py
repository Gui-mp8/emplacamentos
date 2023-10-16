# from abc import ABC, abstractmethod

import requests

# class ResponseSoup(ABC):

#     @abstractmethod
#     def get_response(self) -> requests.Response:
#         pass

# class FipeCode(ResponseSoup):

#     def get_response(self) -> requests.Response:
#         response = requests.get(url='https://www.tabelafipebrasil.com/fipe/carros', headers={"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'})
#         return print(response)

# FipeCode().get_response()

response = requests.post(url="https://veiculos.fipe.org.br/api/veiculos/ConsultarTabelaDeReferencia")
print(response)