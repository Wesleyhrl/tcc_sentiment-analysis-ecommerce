# Sistema de Análise de Sentimentos para Avaliações de Produtos de E-commerce

Este projeto coleta e analisa avaliações de produtos em e-commerce, classificando automaticamente os sentimentos para auxiliar consumidores na tomada de decisão. Os dados são extraídos da plataforma Kabum via **web scraping**, processados com modelos de linguagem pré-treinados e disponibilizados por meio de uma **API REST**, com visualização em interface web em **Next.js**.

## Pré-requisitos

Antes de começar, você precisa ter instalado:

- Python 3.9+
- **Poetry** (Gerenciador de dependências)
- Node.js 22+
- MongoDB
- Navegador Chrome

## Estrutura do repositório

- 1_coleta -> Web Scraping (Kabum)
- 2_analise -> Processamento e Análise de Sentimentos
- 3_backend -> API em FastAPI
- 4_frontend -> Interface Web (Next.js / React)

## Tecnologias Utilizadas

| Camada | Tecnologias |
|-------|-------------|
| Coleta | Selenium, Requests, Lxml |
| Análise | Datasets (Hugging Face), Transformers (HuggingFace), PyTorch, Pandas, Scikit-Learn |
| Backend | FastAPI, Pydantic |
| Frontend | Next.js (React), TailwindCSS, Shadcn UI, Recharts |
| Banco de Dados | MongoDB, PyMongo |


## Instalação das Dependências

### Poetry (Python)

O projeto utiliza **Poetry** para gerenciar as dependências. Siga os passos para configurar o ambiente:

1. Instale o Poetry.
> Para instruções de instalação, consulte a documentação oficial: [https://python-poetry.org/docs/#installing-with-the-official-installer](https://python-poetry.org/docs/#installing-with-the-official-installer)
2. Clone o repositório ou navegue até a pasta do projeto.
3. Instale as dependências usando um dos comandos abaixo, dependendo do hardware da sua máquina:

| Tipo de Máquina | Comando de Instalação | Descrição |
| :--- | :--- | :--- |
| **Máquina CPU (Padrão)** | `poetry install` | Instala todos os pacotes (incluindo PyTorch/Torchvision) da versão CPU-Only do PyPI padrão. |
| **Máquina GPU (CUDA)** | `poetry install --with cuda` | Instala todos os pacotes, mas o PyTorch/Torchvision da seção principal são substituídos pelas versões CUDA da fonte `pytorch-cu129`. |

**Observação:**
* O comando `poetry install` criará automaticamente um ambiente virtual para o projeto.
* Se for necessário ativar o ambiente virtual manualmente, utilize: `poetry env activate`. Este comando imprimirá a linha exata de código que você deve usar para ativar o ambiente, copie e cole a linha de código gerada e execute-a.

### Node

O projeto também utiliza Node.js, execute na raiz para instalar todas as dependências:

```bash
npm run setup
```
## Como Executar

Utilize os scripts configurados no package.json da raiz para facilitar a execução:

1. Garanta que o MongoDB esteja rodando.

2. Executar Coleta de Dados (Scraping):

   * `npm run scrape`

3. Executar Treinamento do Modelo (Fine-tuning - Quando Necessário):

   * `npm run fine-tuning`

4. Executar análise de sentimentos (Processar dados coletados):

   * `npm run analyze`
5. Rodar a Aplicação (Backend + Frontend):

   * `npm run app`
6. Acessos (Após iniciar a aplicação):

   * Frontend: `http://localhost:3000`
   * API Docs (Swagger): `http://localhost:8000/docs`

## Aviso

Este projeto foi desenvolvido para fins acadêmicos e de pesquisa.