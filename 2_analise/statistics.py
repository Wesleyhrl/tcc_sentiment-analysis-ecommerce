import numpy as np
from typing import Dict, Any


def extrair_nota(avaliacao: Dict[str, Any]) -> float | None:
    """
    Extrai a nota numérica da string '5 de 5 estrelas.' → 5.0
    Retorna None se não for possível extrair.
    """
    nota_texto = avaliacao.get("nota")
    if not nota_texto or not isinstance(nota_texto, str):
        return None

    try:
        return float(nota_texto.split(" ")[0].replace(",", "."))
    except (ValueError, IndexError):
        return None


def calcular_estatisticas_produto(produto: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula estatísticas completas do produto:
    - Quantidade, percentual e média de confiança por tipo de sentimento
    - Média global de confiança da IA
    - Sentimento predominante do produto
    """
    avaliacoes = produto.get("avaliacoes", [])
    if not avaliacoes:
        return {}

    notas = []
    labels = []
    scores_por_tipo = {"positive": [], "neutral": [], "negative": []}
    todos_scores = []  # ← acumula todos os scores para a média global

    for a in avaliacoes:
        nota = extrair_nota(a)
        sentimento = a.get("sentimento", {})
        label = sentimento.get("label", "").lower().strip()
        score = sentimento.get("score")

        if nota is not None and label in ["positive", "neutral", "negative"]:
            notas.append(nota)
            labels.append(label)

            # Guarda o score de confiança por tipo e geral
            if isinstance(score, (int, float)):
                scores_por_tipo[label].append(score)
                todos_scores.append(score)

    total = len(labels)
    if total == 0:
        return {}

    # Estatísticas por tipo de sentimento
    estatisticas_sentimentos = {}
    for tipo in ["positive", "neutral", "negative"]:
        qtd = labels.count(tipo)
        percentual = (qtd / total * 100) if total > 0 else 0
        media_conf = np.mean(scores_por_tipo[tipo]) if scores_por_tipo[tipo] else 0

        estatisticas_sentimentos[tipo] = {
            "quantidade": qtd,
            "percentual": round(percentual, 2),
            "media_confianca_ia": round(media_conf, 4)
        }

    # Média global de confiança da IA
    media_confianca_global_ia = np.mean(todos_scores) if todos_scores else 0

    # Sentimento predominante (maior quantidade → desempate por média de confiança)
    sentimento_predominante = max(
        estatisticas_sentimentos.items(),
        key=lambda x: (x[1]["quantidade"], x[1]["media_confianca_ia"])
    )[0]

    # Média geral de notas
    media_nota = np.mean(notas) if notas else 0

    return {
        "total_avaliacoes": total,
        "media_nota": round(media_nota, 2),
        "media_confianca_global_ia": round(media_confianca_global_ia, 4),
        "sentimento_predominante": sentimento_predominante,
        "estatisticas_sentimentos": estatisticas_sentimentos,
    }
