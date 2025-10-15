from typing import Optional
from fastapi import APIRouter, Body, Query, Request, status
from fastapi.responses import JSONResponse
from models.produto_model import ProdutoModel, ProdutoBuscaModel
from services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])



@router.get("/{id}", response_model=ProdutoModel)
async def obter_produto(id: str, request: Request):
    """Obtém detalhes completos de um produto pelo seu ID."""
    service = ProdutoService(request.app.database)
    return await service.buscar_produto_id(id)


@router.get("/buscar/", response_model=list[ProdutoBuscaModel])
async def buscar_produtos(
    request: Request,
    titulo: Optional[str] = Query(
        None, description="Buscar por título"),
    url: Optional[str] = Query(
        None, description="Buscar por URL"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Número máximo de produtos a retornar"),
    skip: Optional[int] = Query(0, ge=0, description="Número de produtos a pular")
):
    """
    Busca produtos por título ou URL.

    - **titulo**: Busca parcial no título do produto (case-insensitive)
    - **url**: Busca parcial na URL do produto (case-insensitive)
    - **limit**: Limita o número de resultados retornados (padrão: 50, máximo: 100)
    - **skip**: Número de resultados a pular (padrão: 0)

    Pode usar apenas um. Retorna apenas informações básicas do produto.
    """
    service = ProdutoService(request.app.database)
    return await service.buscar_produtos(titulo=titulo, url=url, limit=limit, skip=skip)

