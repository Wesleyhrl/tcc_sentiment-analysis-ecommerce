from fastapi import FastAPI
from core.database import lifespan
from routers.produto_router import router

app = FastAPI(title="API de Produtos e Análises", lifespan=lifespan)
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "API de Produtos e Análises ativa!"}