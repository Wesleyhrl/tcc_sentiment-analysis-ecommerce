import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Carrega as variáveis do arquivo .env
load_dotenv()

def get_database():
    """
    Retorna a instância do banco de dados configurada via variáveis de ambiente.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("MONGO_DB_NAME", "kabum_scraping")
    
    try:
        client = MongoClient(mongo_uri)
        return client[db_name]
    except Exception as e:
        raise ConnectionError(f"Falha ao conectar no MongoDB: {e}")