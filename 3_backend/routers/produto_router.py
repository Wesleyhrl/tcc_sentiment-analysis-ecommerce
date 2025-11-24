from typing import Optional, List
from fastapi import APIRouter, Body, Query, Request, status
from fastapi.responses import JSONResponse
from models.produto_model import ProdutoModel, ProdutoBuscaModel
from models.pagination_model import PaginationResponse
from services.produto_service import ProdutoService
from models.navegacao_model import NavegacaoList

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/navegacao/", response_model=NavegacaoList)
async def navegar_categorias(
    request: Request,
    filtro: Optional[str] = Query(
        None, description="Caminho base para buscar as subcategorias (ex: 'hardware/coolers'). Se omitido, retorna os Departamentos raiz.")
):
    """
    Retorna a lista de categorias do próximo nível hierárquico.

    Este endpoint permite navegar na árvore de produtos progressivamente.

    **Como utilizar:**

    * **Nível 1 (Raiz):** * *Requisição:* `GET /produtos/navegacao/` (sem parâmetros).
        * *Retorno:* Lista de Departamentos (ex: "Hardware", "Periféricos").

    * **Nível 2 (Categorias):** * *Requisição:* `GET /produtos/navegacao/?filtro=hardware`
        * *Retorno:* Lista de categorias dentro de Hardware (ex: "Coolers", "SSD").

    * **Nível 3 (Subcategorias):** * *Requisição:* `GET /produtos/navegacao/?filtro=hardware/coolers`
        * *Retorno:* Lista de itens dentro de Coolers (ex: "Fan", "Water Cooler").

    **Nota:** O campo `caminho_completo` da resposta deve ser usado como o valor do parâmetro `filtro` na próxima chamada.
    """
    service = ProdutoService(request.app.database)
    return await service.obter_navegacao(nivel_anterior=filtro)


@router.get("/{id}", response_model=ProdutoModel)
async def obter_produto(id: str, request: Request):
    """Obtém detalhes completos de um produto pelo seu ID."""
    service = ProdutoService(request.app.database)
    return await service.buscar_produto_id(id)

@router.get("/buscar/", response_model=PaginationResponse[ProdutoBuscaModel])
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

@router.get("/listar/localizacao/", response_model=PaginationResponse[ProdutoBuscaModel])
async def listar_produtos_por_localizacao(
    request: Request,
    filtro: str = Query(..., description="Caminho da categoria (ex: 'hardware' ou 'hardware/ssd-2-5')"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Itens por página")
):
    """
    Lista produtos pertencentes a uma categoria específica.
    
    - **filtro**: Parte da URL que representa a categoria (obtido na rota de navegação).
    """
    service = ProdutoService(request.app.database)
    return await service.buscar_produtos_por_localizacao(localizacao=filtro, page=page, page_size=page_size)