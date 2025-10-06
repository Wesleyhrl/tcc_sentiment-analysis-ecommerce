from pymongo import MongoClient
import pandas as pd
import random
import os

# Conexão com o MongoDB (ajuste a URI se necessário)
client = MongoClient("mongodb://localhost:27017/")
db = client["kabum_scraping"]
collection = db["produtos"]

# Buscar todos os documentos da coleção
docs = collection.find({})

# Lista para armazenar avaliações
avaliacoes_texto = set()

for doc in docs:
    for avaliacao in doc.get("avaliacoes", []):
        titulo = avaliacao.get("titulo", "").strip()
        comentario = avaliacao.get("comentario", "").strip()
        
        # Usar join com filter
        texto = ". ".join(filter(None, [titulo, comentario])).strip()
        
        # Só adiciona se tiver algo escrito
        if texto:
            avaliacoes_texto.add(texto)

# Embaralha e pega no máximo 2000 avaliações
avaliacoes_lista = list(avaliacoes_texto)
print(f"Total de avaliações únicas encontradas: {len(avaliacoes_lista)}")
avaliacoes_sample = random.sample(avaliacoes_lista, min(2000, len(avaliacoes_lista)))
print(f"Total de avaliações extraídas: {len(avaliacoes_sample)}")
# Converter em DataFrame
df = pd.DataFrame(avaliacoes_sample, columns=["avaliacao"])

# Criar diretório se não existir
output_dir = "./2_analise/fine-tuning"
os.makedirs(output_dir, exist_ok=True)

# Caminho final do arquivo
output_path = os.path.join(output_dir, "avaliacoes_kabum.csv")

# salvar em CSV
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Arquivo salvo com {len(avaliacoes_sample)} avaliações.")
