import pandas as pd
import asyncio
import aiohttp
import time


class ConsultarAnoModeloPeloCodigoFipe():
    def __init__(self, **kwargs) -> None:
        self.codigo_fipe = kwargs.get("codigo_fipe")
        self.lenght = kwargs.get("lenght")
        self.endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/ConsultarAnoModeloPeloCodigoFipe"

    def get_task(self, session: aiohttp.ClientSession) -> aiohttp.ClientRequest:
        print(f"Working on fipe code: {self.codigo_fipe}")
        payload = {
            'codigoTipoVeiculo': '1',
            'codigoTabelaReferencia': '302',
            'codigoModelo': '',
            'codigoMarca': '',
            'ano': '',
            'codigoTipoCombustivel': '',
            'anoModelo': '',
            'tipoVeiculo': '',
            'modeloCodigoExterno': f'{self.codigo_fipe}',
        }

        return session.post(self.endpoint_url, data=payload)

    def task_list(self, session) -> list:
        tasks = [
            self.get_task(session) for _ in range(self.lenght)
        ]
        return tasks

    async def get_endpoint_data(self) -> list:
        data = []
        async with aiohttp.ClientSession() as session:
            tasks = self.task_list(session)
            responses = await asyncio.gather(*tasks)
            for response in responses:
                if response.status == 200:
                    data.extend(await response.json())
                else:
                    print("Skipping response")

        return data

df = pd.read_json("./data/2023-10/fipe_codes_2023-10.json")
for index, row in df.iterrows():
    asyncio.run(
        ConsultarAnoModeloPeloCodigoFipe(
            codigo_fipe = row.iloc[0],
            lenght=len(df)
        ).get_endpoint_data
    )
