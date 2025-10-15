from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da conexão MongoDB"""
    app.mongodb_client = AsyncMongoClient(settings.MONGODB_URL)
    app.database = app.mongodb_client[settings.MONGODB_DB_NAME]
    ping_response = await app.database.command("ping")

    if int(ping_response["ok"]) != 1:
        raise Exception("Falha na conexão com o cluster MongoDB.")

    yield
    await app.mongodb_client.close()
