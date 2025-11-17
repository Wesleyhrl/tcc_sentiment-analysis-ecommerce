from transformers import pipeline
from typing import Dict, Any, List


class SentimentAnalyzer:

    def __init__(self, model_name, device="cpu"):
        self.pipe = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=device,
            return_all_scores=True,
            top_k=None
        )

    def preparar_texto_analise(self, titulo: str, comentario: str) -> str:
        """Prepara texto otimizado para análise de sentimentos"""
        titulo = titulo.strip() if titulo else ""
        comentario = comentario.strip() if comentario else ""

        # Se ambos existem, junta com pontuação
        if titulo and comentario:
            return f"{titulo}. {comentario}"
        # Se só tem um, retorna ele mesmo
        elif titulo:
            return titulo
        elif comentario:
            return comentario
        else:
            return ""

    def analisar_avaliacao(self, titulo: str, comentario: str) -> Dict[str, Any]:
        """
        Analisa uma avaliação usando título + comentário concatenados.
        """
        texto = self.preparar_texto_analise(titulo, comentario)

        if not texto or texto == ".":
            return {"label": "sem_texto", "score": 1.0}

        resultado = self.pipe(texto)[0]
        melhor = max(resultado, key=lambda x: x["score"])

        return {
            "label": melhor["label"],
            "score": round(float(melhor["score"]), 4),
            # "detalhado": resultado
        }

    def analisar_avaliacoes_em_lote(self, avaliacoes: List[Dict]) -> List[Dict]:
        """
        Analisa todas as avaliações de um produto em lote e retorna
        o array de avaliações já com os sentimentos incluídos.
        """
        textos = []
        indices_validos = []

        # Prepara os textos e guarda os índices dos textos válidos
        for i, avaliacao in enumerate(avaliacoes):
            titulo = avaliacao.get("titulo", "")
            comentario = avaliacao.get("comentario", "")
            texto = self.preparar_texto_analise(titulo, comentario)

            if texto and texto != ".":
                textos.append(texto)
                indices_validos.append(i)

        # Processa todos os textos válidos de uma vez
        if textos:
            resultados = self.pipe(textos)

            # Atribui os resultados diretamente às avaliações
            for idx, resultado in zip(indices_validos, resultados):
                melhor = max(resultado, key=lambda x: x["score"])
                avaliacoes[idx]["sentimento"] = {
                    "label": melhor["label"],
                    "score": round(float(melhor["score"]), 4),
                }

        # Para avaliações sem texto válido, atribui sentimento padrão
        for i, avaliacao in enumerate(avaliacoes):
            if "sentimento" not in avaliacao:
                avaliacao["sentimento"] = {"label": "sem_texto", "score": 1.0}

        return avaliacoes
