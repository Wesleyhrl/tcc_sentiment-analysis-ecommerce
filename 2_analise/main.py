import torch
from mongo_handler import carregar_produtos, salvar_produto_analisado
from sentiment_analysis_model import SentimentAnalyzer
from statistics import calcular_estatisticas_produto

from pathlib import Path

MODEL_DIR = "fine-tuning/caramelo-smile-kabum-finetuned" 

# Obter o caminho absoluto para o diretório do modelo
base_dir = Path(__file__).parent 
model_path_absolute = base_dir / MODEL_DIR
model_name = str(model_path_absolute.resolve()) # Garante que é um caminho absoluto limpo


def main():
    produtos = carregar_produtos()

    if torch.cuda.is_available():
        device = "cuda"
        print("GPU CUDA detectada. Usando 'cuda' para processamento.")
    else:
        device = "cpu"
        print("GPU CUDA não encontrada. Usando 'cpu' para processamento.")
    
    analyzer = SentimentAnalyzer(model_name=model_name, device=device)

    for produto in produtos:
        avaliacoes = produto.get("avaliacoes", [])
        
        if avaliacoes:
            # Analisa e retorna as avaliações já com sentimentos
            produto["avaliacoes"] = analyzer.analisar_avaliacoes_em_lote(avaliacoes)

        # Calcula estatísticas do produto analisado
        estatisticas = calcular_estatisticas_produto(produto)
        produto["estatisticas"] = estatisticas  

        # salva no banco de análises
        salvar_produto_analisado(produto)


if __name__ == "__main__":
    main()
