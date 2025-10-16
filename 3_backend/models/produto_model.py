from typing import List, Optional
from pydantic import BaseModel, Field

class SentimentoModel(BaseModel):
    label: str
    score: float

class AvaliacaoModel(BaseModel):
    id: int
    pagina: int
    autor: str
    nota: Optional[str] = None
    data: Optional[str] = None
    titulo: Optional[str] = None
    comentario: Optional[str] = None
    sentimento: SentimentoModel

class ProdutoInfoModel(BaseModel):
    titulo: str
    localizacao: Optional[str] = None
    codigo: Optional[str] = None
    loja: Optional[str] = None
    descricao: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    classificacao: Optional[float] = None
    total_avaliacoes_coletadas: Optional[int] = 0
    url: Optional[str] = None
    data_extracao: Optional[str] = None

class EstatisticaSentimentoModel(BaseModel):
    quantidade: Optional[int] = 0
    percentual: Optional[float] = 0.0
    media_confianca_ia: Optional[float] = 0.0

class EstatisticasModel(BaseModel):
    total_avaliacoes: Optional[int] = 0
    media_nota: Optional[float] = 0.0
    media_confianca_global_ia: Optional[float] = 0.0
    sentimento_predominante: Optional[str] = None
    assimiliacao_nota_sentimento: Optional[float] = None
    estatisticas_sentimentos: Optional[dict[str, EstatisticaSentimentoModel]] = {}

class ProdutoModel(BaseModel):
    id: str = Field(alias="_id")
    avaliacoes: Optional[List[AvaliacaoModel]] = []
    produto: ProdutoInfoModel
    estatisticas: Optional[EstatisticasModel] = EstatisticasModel()

class ProdutoBuscaModel(BaseModel):
    id: str = Field(alias="_id")
    produto: ProdutoInfoModel


class IdOutModel(BaseModel):
    id: str = Field(alias="_id")