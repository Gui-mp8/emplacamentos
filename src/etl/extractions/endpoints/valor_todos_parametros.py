from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import asyncio
from aiohttp import ClientSession

from models.tabela_fipe import TabelaFipe
from abstractions.asyncio_endpoints_abstraction import AsyncEndpoint

class ConsultarValorComTodosParametros(AsyncEndpoint):

    def task_list(self, session: ClientSession) -> list and str:
        """
            This method returns a list of tasks for each fipe code to be conclued using
            asyncio

            Args:
                session (ClientSession): it's an aiohttp class

            Returns:
                list: It's the task list
                str: it's a string that represents the actual month of the extraction
        """
        tasks = []
        for index, row in self.dataframe.iterrows():
        # for code in fipe_codes:
            print(f"Working on fipe code: {row.iloc[4]}")
            payload = {
                'codigoTabelaReferencia': f'{row.iloc[3]}',
                'codigoMarca': '',
                'codigoModelo': '',
                'codigoTipoVeiculo': '1',
                'anoModelo': f'{row.iloc[1]}',
                'codigoTipoCombustivel': f'{row.iloc[2]}',
                'tipoVeiculo': 'carro',
                'modeloCodigoExterno': f'{row.iloc[4]}',
                'tipoConsulta': 'codigo'
            }
            mes_referencia = row.iloc[5]

            tasks.append(session.post(self.endpoint_url, data=payload, ssl=False))

        return tasks, mes_referencia

    async def get_endpoint_data(self) -> List[Dict[str, Any]]:
        """
            This method gets the endpoint data for each task in a task list and
            pass it to a list.
        """
        data = []
        async with ClientSession() as session:
            tasks, mes_referencia = self.task_list(session)  # Unpack the return values
            responses = await asyncio.gather(*tasks)
            for response in responses:
                if response.status == 200:
                    json_data = await response.json()
                    carros = TabelaFipe(
                        valor=json_data["Valor"].split(" ")[1].replace(".", "").replace(',', '.'),
                        marca=json_data["Marca"],
                        modelo=json_data["Modelo"],
                        ano_modelo=json_data["AnoModelo"],
                        combustivel=json_data["Combustivel"],
                        codigo_fipe=json_data["CodigoFipe"],
                        mes_referencia=mes_referencia,
                        extraction_date=datetime.now().strftime("%Y-%m-%d")
                    )
                    data.append(carros.model_dump())
                else:
                    print(f"Skipping fipe code {json_data['CodigoFipe']} response")

        return data