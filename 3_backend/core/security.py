# core/security.py
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from core.config import settings

# Define que a chave deve vir no header com o nome "X-API-Key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def validar_api_key(key: str = Security(api_key_header)):
    """
    Verifica se a API Key fornecida no header corresponde à chave do sistema.
    """
    if key == settings.API_KEY:
        return key
    
    
    # Se a chave estiver errada ou faltando, retorna erro 403 (Proibido)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Credenciais de autenticação inválidas ou ausentes."
    )