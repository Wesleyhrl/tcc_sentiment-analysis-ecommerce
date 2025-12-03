# Sistema de Análise de Sentimentos para Avaliações de Produtos de E-commerce

Este projeto coleta e analisa avaliações de produtos em e-commerce, classificando automaticamente os sentimentos para auxiliar consumidores na tomada de decisão. Os dados são extraídos da plataforma Kabum via **web scraping**, processados com modelos de linguagem pré-treinados e disponibilizados por meio de uma **API REST**, com visualização em interface web em **Next.js**.

> 🌐 **Demonstração Online:** Acesse o projeto em execução em **[https://reviewsentimentum.vercel.app/](https://reviewsentimentum.vercel.app/)**

## Pré-requisitos

Antes de começar, você precisa ter instalado:

- Python 3.13+
- **Poetry** (Gerenciador de dependências)
- Node.js 22+
- MongoDB
- Navegador Chrome

## Estrutura do repositório

Cada módulo possui sua própria documentação detalhada. Clique nos links abaixo para ver os detalhes de implementação de cada etapa:

- [**1_coleta**](./1_coleta/README.md) -> Web Scraping (Kabum) e Persistência de dados brutos.
- [**2_analise**](./2_analise/README.md) -> Processamento, Fine-tuning e Classificação de Sentimentos.
- [**3_backend**](./3_backend/README.md) -> API REST em FastAPI e acesso ao MongoDB.
- [**4_frontend**](./4_frontend/sentiment-analysis-frontend/README.md) -> Interface Web (Next.js / React) para visualização dos dados.


🧠 [**Clique aqui para ver fine-tuning do Modelo (Jupyter Notebook)**](./2_analise/fine-tuning/fine_tuning.ipynb)

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
## Configuração de Ambiente (.env)

Para que a comunicação entre o Frontend e o Backend funcione localmente, é necessário configurar as chaves de acesso.

1.  **Backend:** Crie um arquivo `.env` dentro da pasta `3_backend`:

    ```env
    API_KEY="key-local"
    ```

2.  **Frontend:** Crie um arquivo `.env` dentro da pasta `4_frontend/sentiment-analysis-frontend`:

    ```env
    API_KEY="key-local"
    ```

## Como Executar

Utilize os scripts configurados no `package.json` da raiz para facilitar a execução:

1. Garanta que o MongoDB esteja rodando e esteja com ambiente virtual ativado.

2. **Executar Coleta de Dados (Scraping):**

   * `npm run scrape`

3. **Executar Treinamento do Modelo (Fine-tuning - Quando Necessário):**

   * `npm run fine-tuning`

4. **Executar Análise de Sentimentos (Processar dados coletados):**

   * `npm run analyze`
5. **Rodar a Aplicação (Backend + Frontend):**

   * `npm run app`
6. **Rodar a Aplicação Separadamente (Opcional):**

   Caso prefira rodar em terminais diferentes:
   * Backend: `npm run start-backend`
   * Frontend: `npm run start-frontend`
7. Acessos (Após iniciar a aplicação):

   * Frontend: `http://localhost:3000`
   * API Docs (Swagger): `http://localhost:8000/docs`

## Referência

**Modelo utilizado:**

Dantas, A. C. (2024). *caramelo-smile* (Revision 2707a19). Hugging Face.  
Disponível em: https://huggingface.co/Adilmar/caramelo-smile  
DOI: 10.57967/hf/2061

## Aviso

Este projeto foi desenvolvido para fins acadêmicos e de pesquisa.
