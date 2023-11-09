from abc import ABC, abstractmethod
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from abstractions.site_scraper_abstraction import SiteScraper

class FipeCode(SiteScraper):
    def __init__(self) -> None:
        self.parser = "html.parser"

    def get_response(self) -> requests.Response:
        response = requests.get(url=self.url_base, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"HTTP request failed with status code {response.status_code}")
        return response

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.get_response().content, self.parser)

    def get_soup_data(self) -> List[Dict[str, str]]:
        soup = self.get_soup()
        fipe_data= []

        for a_tag in soup.find_all('a', title=True):
            if a_tag.get('title').startswith("Tabela FIPE código"):
                code = a_tag.text
                car_model = a_tag.find_next('a', title=True).text
                data_dict = {'code': code, 'car_models': car_model}
                fipe_data.append(data_dict)

        return fipe_data


# if __name__ == "__main__":
#     base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
#     headers = {"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
#     fipe = FipeCode()
#     fipe.url_base = base_url
#     fipe.headers = headers
#     print(fipe.get_soup_data()["code"])