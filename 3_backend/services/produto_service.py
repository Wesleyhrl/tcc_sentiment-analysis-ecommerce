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

    async def buscar_produtos(self, titulo: str, limit: int = 50, skip: int = 0):
        # Construir query base
        query = {}

        query["produto.titulo"] = {
            "$regex": titulo,  "$options": "i"}  # case-insensitive

        # Se nenhum parâmetro foi fornecido
        if not query:
            raise HTTPException(
                status_code=400,
                detail="É necessário fornecer pelo menos um parâmetro de busca (titulo ou url)"
            )

        # Projeção para excluir campos desnecessários e otimizar a consulta
        projection = {
            "avaliacoes": 0,
            "estatisticas": 0,
        }

        # Executar a busca
        produtos = await self.collection.find(query, projection).skip(skip).limit(limit).to_list()

        if not produtos:
            raise HTTPException(
                status_code=404,
                detail="Nenhum produto encontrado com os critérios fornecidos"
            )

        return produtos
