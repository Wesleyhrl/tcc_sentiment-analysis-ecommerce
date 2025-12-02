from fastapi import Depends, FastAPI
from core.database import lifespan
from routers.produto_router import router
from core.security import validar_api_key

app = FastAPI(title="API de Produtos e Análises", lifespan=lifespan)
app.include_router(router, dependencies=[Depends(validar_api_key)])

@app.get("/")
async def root():
    return {"status": "API de Produtos e Análises ativa!"}