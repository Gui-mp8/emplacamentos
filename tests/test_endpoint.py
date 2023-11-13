import requests

def test_endpoint_tabela_referencia():
    response = requests.post("https://veiculos.fipe.org.br/api/veiculos/ConsultarTabelaDeReferencia")

    assert response.status_code==200

def test_endpoint_tabela_ano_modelo():
    payload = {
        'codigoTipoVeiculo': '1',
        'codigoTabelaReferencia': '302',
        'codigoModelo': '',
        'codigoMarca': '',
        'ano': '',
        'codigoTipoCombustivel': '',
        'anoModelo': '',
        'tipoVeiculo': '',
        'modeloCodigoExterno': '029157-9',
    }
    response = requests.post("https://veiculos.fipe.org.br/api/veiculos/ConsultarAnoModeloPeloCodigoFipe", data=payload)

    assert response.status_code==200

def test_endpoint_tabela_todos_parametros():
    payload = {
        'codigoTabelaReferencia': '302',
        'codigoMarca': '',
        'codigoModelo': '',
        'codigoTipoVeiculo': '1',
        'anoModelo': '2024',
        'codigoTipoCombustivel': '1',
        'tipoVeiculo': 'carro',
        'modeloCodigoExterno': '029157-9',
        'tipoConsulta': 'codigo'
    }
    response = requests.post("https://veiculos.fipe.org.br/api/veiculos/ConsultarValorComTodosParametros", data=payload)

    assert response.status_code==200