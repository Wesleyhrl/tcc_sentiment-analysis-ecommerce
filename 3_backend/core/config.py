import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "produtos_analises")
    API_KEY = os.getenv("API_KEY")

settings = Settings()
