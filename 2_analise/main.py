from mongo_handler import carregar_produtos, salvar_produto_analisado
from sentiment_analysis_model import SentimentAnalyzer
from statistics import calcular_estatisticas_produto


def main():
    produtos = carregar_produtos()
    analyzer = SentimentAnalyzer()

    for produto in produtos[:10]:
        for avaliacao in produto.get("avaliacoes", []):
            sentimento = analyzer.analisar_avaliacao(
                avaliacao.get("titulo", ""),
                avaliacao.get("comentario", "")
            )
            avaliacao["sentimento"] = sentimento

        # Calcula estatísticas do produto analisado
        estatisticas = calcular_estatisticas_produto(produto)
        produto["estatisticas"] = estatisticas  

        # salva no banco de análises
        salvar_produto_analisado(produto)


if __name__ == "__main__":
    main()
