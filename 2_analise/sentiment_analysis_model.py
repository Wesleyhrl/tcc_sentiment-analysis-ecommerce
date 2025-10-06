from transformers import pipeline
from typing import Dict, Any


class SentimentAnalyzer:

    def __init__(self, model_name="./2_analise/fine-tuning/caramelo-smile-kabum-finetuned", device="cuda"):
        self.pipe = pipeline("sentiment-analysis",
                             model=model_name, device=device, return_all_scores=True, top_k=None)
    # def __init__(self, model_name="Adilmar/caramelo-smile-2", device="cuda"):
    #    self.pipe = pipeline(
    #        "text-classification",
    #        model=model_name,
    #        device=device,
    #        return_all_scores=True,
    #        top_k=None
    #    )

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