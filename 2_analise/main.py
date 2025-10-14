from mongo_handler import carregar_produtos, salvar_produto_analisado
from sentiment_analysis_model import SentimentAnalyzer
from statistics import calcular_estatisticas_produto


def main():
    produtos = carregar_produtos()
    analyzer = SentimentAnalyzer()

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
