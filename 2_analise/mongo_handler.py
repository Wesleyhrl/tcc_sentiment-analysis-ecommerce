from pymongo import MongoClient
from typing import List, Dict, Any

# Banco de onde vêm os dados originais
CONNECTION_STRING = "mongodb://localhost:27017/"
DB_SCRAPING = "kabum_scraping"
COLLECTION_SCRAPING = "produtos"

# Banco onde será salvo o resultado da análise
DB_ANALYSIS = "produtos_analises"
COLLECTION_ANALYSIS = "produtos"


def get_collection(db_name: str, collection_name: str):
    """Retorna uma coleção específica do MongoDB."""
    client = MongoClient(CONNECTION_STRING)
    db = client[db_name]
    return db[collection_name]


def carregar_produtos() -> List[Dict[str, Any]]:
    """Carrega todos os produtos do banco de scraping."""
    collection = get_collection(DB_SCRAPING, COLLECTION_SCRAPING)
    resultados = list(collection.find({}))
    
    print(f"Total de produtos carregados: {len(resultados)}")
    total_avaliacoes = sum(doc.get("produto", {}).get("total_avaliacoes_coletadas", 0) for doc in resultados)
    print(f"Total de avaliações: {total_avaliacoes}")
    
    return resultados


def salvar_produto_analisado(produto: Dict[str, Any]):
    """
    Salva o produto analisado no banco de análises.
    Se já existir pelo _id, substitui.
    """
    collection = get_collection(DB_ANALYSIS, COLLECTION_ANALYSIS)
    collection.replace_one({"_id": produto["_id"]}, produto, upsert=True)
    print(f"Produto {produto['_id']} salvo em {DB_ANALYSIS}.{COLLECTION_ANALYSIS}")
