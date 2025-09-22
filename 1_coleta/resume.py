import datetime
import os
from pymongo import MongoClient

# Variáveis globais para armazenar as estatísticas
start_time = None
total_urls = 0
produtos_processados = 0
total_erros = 0
nome_arquivo = ""

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["kabum_scraping"]
collection = db["estatisticas"]

def iniciar_estatisticas():
    """Inicia o registro do tempo de execução e cria arquivo inicial"""
    global start_time, nome_arquivo
    start_time = datetime.datetime.now()
    
    # Cria nome do arquivo com data atual
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"estatisticas_{data_atual}"
    
    # Salva as estatísticas iniciais no MongoDB
    salvar_estatisticas()

def atualizar_estatisticas(urls_carregadas=None, processados=None, erros=None):
    """Atualiza as estatísticas e salva no MongoDB"""
    global total_urls, produtos_processados, total_erros
    
    if urls_carregadas is not None:
        total_urls = urls_carregadas
    if processados is not None:
        produtos_processados = processados
    if erros is not None:
        total_erros = erros
    
    # Salva imediatamente no MongoDB
    salvar_estatisticas()

def salvar_estatisticas():
    """Salva as estatísticas atuais no MongoDB"""
    if start_time is None or not nome_arquivo:
        return
    
    # Calcula o tempo total de execução
    tempo_total = datetime.datetime.now() - start_time
    minutos_total = round(tempo_total.total_seconds() / 60, 2)
    
    # Cria o documento JSON para ser inserido
    estatisticas_doc = {
        "id_sessao": nome_arquivo,
        "data_inicial": start_time,
        "total_urls_carregadas": total_urls,
        "produtos_processados": produtos_processados,
        "total_erros": total_erros,
        "tempo_total_minutos": minutos_total
    }
    
    try:
        # Tenta atualizar um documento existente ou cria um novo se não encontrar
        collection.update_one(
            {"id_sessao": nome_arquivo},
            {"$set": estatisticas_doc},
            upsert=True
        )
        print("Estatísticas salvas no MongoDB com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar estatísticas no MongoDB: {e}")