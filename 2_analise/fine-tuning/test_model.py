from transformers import pipeline

# Carregar o modelo fine-tuned
classifier = pipeline("sentiment-analysis",
                      model="./2_analise/fine-tuning/caramelo-smile-kabum-finetuned")

# Textos para analisar
textos = [
    "PRODUTO BOM POREM... PRODUTO MUITO BOM PORÉM A QUANTIDADE REAL DE ARMAZENAMENTO NAO É A QUE É DIVULGADA NA EMBALAGEM. É MENOR!",
    "Não gostei, veio com defeito.",
    "Entrega rápida, produto conforme descrito.",
    "Péssimo e Barulhento, não recomendo.",
    "Produto ok, mas também produto não é bom.",
]

# Analisar sentimentos
for texto in textos:
    resultado = classifier(texto)[0]
    print(f"Texto: {texto}")
    print(
        f"Sentimento: {resultado['label']} | Confiança: {resultado['score']}")
    print("-" * 10)
