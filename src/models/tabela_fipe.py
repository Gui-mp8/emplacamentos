from pydantic import BaseModel

class TabelaFipe(BaseModel):
    valor: str
    marca: str
    modelo: str
    ano_modelo: int
    combustivel: str
    codigo_fipe: str
    mes_referencia: str
    extraction_date: str