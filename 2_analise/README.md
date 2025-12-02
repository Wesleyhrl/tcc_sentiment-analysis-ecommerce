# Módulo de Análise de Sentimentos

Este módulo é o coração do sistema, responsável por realizar a análise de sentimentos sobre as avaliações de produtos coletadas na etapa anterior. Ele utiliza um modelo de linguagem da Hugging Face, que foi refinado (fine-tuned) especificamente com dados do e-commerce em questão (Kabum!), para classificar as avaliações em `positivas`, `negativas` ou `neutras`.

O processo consiste em carregar os dados brutos do MongoDB, submetê-los ao modelo de análise, calcular um conjunto detalhado de estatísticas e, por fim, salvar os dados enriquecidos em um novo banco de dados para serem consumidos pelo backend.

## Funcionalidades

- **Análise de Sentimento em Lote**: Processa todas as avaliações de um produto de forma otimizada.
- **Modelo Fine-Tuned**: Utiliza o modelo `Adilmar/caramelo-smile-2` como base, ajustado com avaliações reais para entender melhor o contexto de produtos de tecnologia.
- **Aceleração por GPU**: Detecta e utiliza automaticamente uma GPU com CUDA, se disponível, para acelerar o processo de análise.
- **Cálculo de Estatísticas**: Gera métricas importantes para cada produto, como:
  - Distribuição de sentimentos (quantidade e percentual).
  - Média de confiança do modelo por tipo de sentimento.
  - Sentimento predominante.
  - Média geral das notas (estrelas).
  - Uma métrica de "assimilação", que compara o sentimento previsto pela IA com a nota em estrelas dada pelo usuário.
- **Persistência de Dados**: Salva os resultados em uma coleção separada no MongoDB, pronta para ser servida pela API.

## Estrutura de Arquivos

```
2_analise/
│
├── main.py                     # Script principal que orquestra todo o processo de análise.
├── mongo_handler.py            # Gerencia a conexão e as operações com o MongoDB.
├── sentiment_analysis_model.py # Classe que encapsula o pipeline de análise de sentimentos.
├── statistics.py               # Funções para calcular as estatísticas dos resultados.
│
└── fine-tuning/                # Diretório com todo o material para o fine-tuning do modelo.
    ├── extract.py              # Script para extrair avaliações do MongoDB e criar um dataset.
    ├── fine_tuning.py          # Script que executa o treinamento e fine-tuning do modelo.
    ├── avaliacoes_kabum.csv    # Dataset de avaliações extraídas (sem labels).
    ├── avaliacoes_kabum_sentimento.csv # Dataset final com labels, usado para o treino.
    └── caramelo-smile-kabum-finetuned/ # Modelo fine-tuned salvo e pronto para uso.
```

## Bibliotecas Utilizadas

- `torch` & `torchvision`: Framework de deep learning para rodar o modelo.
- `transformers`: Para carregar e utilizar o modelo de linguagem da Hugging Face.
- `datasets`: Para manipulação de dados durante o fine-tuning.
- `pymongo`: Driver para comunicação com o banco de dados MongoDB.
- `pandas`: Utilizado para manipulação de dados no processo de fine-tuning.
- `scikit-learn`: Para divisão de dados e cálculo de métricas no fine-tuning.
- `numpy`: Para operações numéricas no cálculo de estatísticas.
- `accelerate`: Otimiza o treinamento em diferentes hardwares (CPU/GPU).

## Pré-requisitos

- Python
- Poetry para gerenciamento de dependências.
- Uma instância do MongoDB em execução.
- (Opcional, mas recomendado) Uma GPU NVIDIA com suporte a CUDA para processamento acelerado.

## Instalação

1.  Navegue até o diretório **raiz** do projeto.

2.  Verifique o arquivo `README.md` na pasta raiz para confirmar as dependências e requisitos de instalação.

## Instruções de Uso

1.  Siga as instruções no arquivo `README.md` no diretório **raiz** para os comandos de execução.

2.  Aguarde o processo ser finalizado. O script exibirá o progresso no terminal, indicando se está usando CPU ou GPU e salvando cada produto analisado.
3.  Ao final, os resultados estarão disponíveis no banco de dados `produtos_analises`, coleção `produtos`.


