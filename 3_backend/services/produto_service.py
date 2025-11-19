import math
from typing import Optional
from fastapi import HTTPException
from pymongo import ReturnDocument


class ProdutoService:
    def __init__(self, db):
        self.collection = db.get_collection("produtos")

    async def buscar_produto_id(self, id: str):
        produto = await self.collection.find_one({"_id": id})
        if produto:
            return produto
        raise HTTPException(
            status_code=404, detail=f"Produto {id} não encontrado")

    async def buscar_produto_url(self, url: str):

        projection = {
            "_id": 1
        }

        produto = await self.collection.find_one({"produto.url": url}, projection)
        if produto:
            return produto
        raise HTTPException(
            status_code=404, detail=f"Produto com URL {url} não encontrado")

    async def buscar_produtos(self, titulo: str, page: int, page_size: int):
        # Construir query base
        query = {}
        palavras = titulo.split()
        busca_formatada = " ".join([f'"{p}"' for p in palavras])
        
        # Agora passamos a string cheia de aspas para o banco
        query = {"$text": {"$search": busca_formatada}}

        # Contagem (usando índice)
        total_items = await self.collection.count_documents(query)

        # Se nenhum parâmetro foi fornecido
        if not query:
            raise HTTPException(
                status_code=400,
                detail="É necessário fornecer pelo menos um parâmetro de busca (titulo)."
            )

        if total_items == 0:
            return {
                "items": [],
                "total": 0,
                "page": page,
                "size": page_size,
                "pages": 0
            }

        # Projeção para excluir campos desnecessários e otimizar a consulta
        projection = {
            "avaliacoes": 0,
            "estatisticas": 0,
        }

        skip = (page - 1) * page_size

        # Executar a busca
        cursor = self.collection.find(query, projection).skip(skip).limit(page_size)
        produtos = await cursor.to_list(length=page_size)

        # cálculos da paginação
        total_pages = math.ceil(total_items / page_size)

        return {
            "items": produtos,
            "total": total_items,
            "page": page,
            "size": page_size,
            "pages": total_pages
        }