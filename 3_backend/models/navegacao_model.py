
from typing import List
from pydantic import BaseModel


class NavegacaoItem(BaseModel):
    nome_exibicao: str
    caminho_completo: str

NavegacaoList = List[NavegacaoItem]