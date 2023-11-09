import pandas as pd
import asyncio
import aiohttp
import time

df = pd.read_json("./data/2023-10/fipe_codes_2023-10.json")
data = []

async def get_ano_modelo():
    async with aiohttp.ClientSession() as session:
        for index, row in df.head(10).iterrows():
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
            response = await session.post(url,data=payload, ssl=False)

            data.append(await response.json())
        print(data)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_ano_modelo)
# loop.close()
start_time = time.time()  # Record the start time

asyncio.run(get_ano_modelo()) # E a msm coisa do que encima

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time  # Calculate the elapsed time