import math
import re
from typing import Optional
from fastapi import HTTPException
from pymongo import ReturnDocument
from utils.localizacao_utils import extrair_partes_url

class ProdutoService:
    def __init__(self, db):
        self.collection = db.get_collection("produtos")

    async def obter_navegacao(self, nivel_anterior: str = None):
        """
        Usa 'distinct' do MongoDB para buscar apenas caminhos únicos, sem carregar produtos.
        """
        
        # Define o filtro (Regex)
        # Se o nivel_anterior for "hardware", buscamos tudo que tem "hardware" na URL
        query = {}
        if nivel_anterior:
            # O regex garante que estamos olhando dentro da pasta certa
            query["produto.localizacao"] = {"$regex": f".*/{nivel_anterior}/.*"}

        # DISTINCT Mongo retorna apenas as strings de localização únicas.
        urls_unicas = await self.collection.distinct("produto.localizacao", query)

        # Processamento Rápido em Python (String Parsing)
        categorias_encontradas = set()
        
        # Define qual índice da URL queremos pegar (o próximo nível)
        indice_alvo = 0
        if nivel_anterior:
            partes_anteriores = extrair_partes_url(nivel_anterior)
            indice_alvo = len(partes_anteriores)

        resultado = []

        for url in urls_unicas:
            # Usa sua função utilitária existente
            partes = extrair_partes_url(url)
            
            # Verifica se a URL tem profundidade para ter um filho
            if len(partes) > indice_alvo:
                nome_categoria = partes[indice_alvo]
                
                # O 'set' garante que não adicionaremos "coolers" duas vezes
                if nome_categoria not in categorias_encontradas:
                    categorias_encontradas.add(nome_categoria)
                    
                    # Monta o objeto de resposta
                    caminho_completo = f"{nivel_anterior}/{nome_categoria}" if nivel_anterior else nome_categoria
                    
                    resultado.append({
                        "nome_exibicao": nome_categoria,
                        "caminho_completo": caminho_completo
                    })

        # Ordena alfabeticamente
        resultado.sort(key=lambda x: x["nome_exibicao"])
        
        return resultado

    async def buscar_produto_id(self, id: str):
        produto = await self.collection.find_one({"_id": id})
        if produto:
            return produto
        raise HTTPException(
            status_code=404, detail=f"Produto {id} não encontrado")

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
                "page_size": page_size,
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
            "page_size": page_size,
            "pages": total_pages
        }

    async def buscar_produtos_por_localizacao(self, localizacao: str, page: int, page_size: int):
            """
            Busca produtos que contenham o trecho da localização na URL.
            Ex: localizacao="hardware" trará itens com URL ".../hardware/..."
            """
            
            # Escapar caracteres especiais para evitar erro no Regex e garantir segurança
            localizacao_escapada = re.escape(localizacao)

            # Regex: Procura pelo termo precedido por uma barra (para garantir que é uma pasta)
            query = {"produto.localizacao": {"$regex": f".*/{localizacao_escapada}", "$options": "i"}}

            # Contagem total para paginação
            total_items = await self.collection.count_documents(query)

            if total_items == 0:
                return {
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size,
                    "pages": 0
                }

            # Projeção otimizada (igual à busca por título)
            projection = {
                "avaliacoes": 0,
                "estatisticas": 0,
            }

            skip = (page - 1) * page_size

            # Executa a query ordenando por classificação ou titulo (opcional, aqui pus padrão)
            cursor = self.collection.find(query, projection).skip(skip).limit(page_size)
            produtos = await cursor.to_list(length=page_size)

            total_pages = math.ceil(total_items / page_size)

            return {
                "items": produtos,
                "total": total_items,
                "page": page,
                "page_size": page_size,
                "pages": total_pages
            }        