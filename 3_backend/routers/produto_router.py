from typing import Optional
from fastapi import APIRouter, Body, Query, Request, status
from fastapi.responses import JSONResponse
from models.produto_model import ProdutoModel, ProdutoBuscaModel, IdOutModel
from models.pagination_model import PaginationResponse
from services.produto_service import ProdutoService

router = APIRouter(prefix="/produtos", tags=["Produtos"])



@router.get("/{id}", response_model=ProdutoModel)
async def obter_produto(id: str, request: Request):
    """Obtém detalhes completos de um produto pelo seu ID."""
    service = ProdutoService(request.app.database)
    return await service.buscar_produto_id(id)


@router.get("/url/", response_model=IdOutModel)
async def obter_id_produto_pela_url(request: Request, url: str = Query(description="Buscar por URL")):
    """Obtém o ID de um produto pela sua URL."""
    service = ProdutoService(request.app.database)
    return await service.buscar_produto_url(url)


@router.get("/buscar/", response_model= PaginationResponse[ProdutoBuscaModel])
async def buscar_produtos(
    request: Request,
    titulo: str = Query(..., description="Buscar por título"),
    page: int = Query(1, ge=1, description="Número da página (começa em 1)"),
    page_size: int = Query(50, ge=1, le=100, description="Itens por página")
):
    """
    Busca produtos por título com paginação.
    - **titulo**: Busca parcial no título do produto (case-insensitive)
    - **page**: Número da página atual (começa em 1)
    - **page_size**: Número de itens por página (padrão: 50, máximo: 100)
    """
    service = ProdutoService(request.app.database)
    return await service.buscar_produtos(titulo=titulo, page=page, page_size=page_size)