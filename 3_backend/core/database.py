from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import TEXT, AsyncMongoClient
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da conexão MongoDB"""
    app.mongodb_client = AsyncMongoClient(settings.MONGODB_URL)
    app.database = app.mongodb_client[settings.MONGODB_DB_NAME]
    ping_response = await app.database.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Falha na conexão com o cluster MongoDB.")
    
    # Criação de indices
    produtos_collection = app.database.get_collection("produtos")
    
    # Cria índice de TEXTO no campo 'produto.titulo' para buscas rápidas
    await produtos_collection.create_index([("produto.titulo", TEXT)], name="idx_text_produto_titulo")
    # Cria um índice de ordenação ascendente no campo 'produto.localizacao' para consultas rápidas por localização.
    await produtos_collection.create_index([("produto.localizacao", 1)])
    
    print("Conexão com MongoDB estabelecida e índices verificados/criados.")

    yield
    await app.mongodb_client.close()
