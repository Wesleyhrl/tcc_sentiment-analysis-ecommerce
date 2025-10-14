# Sistema de Análise de Sentimentos para Avaliações de Produtos de E-commerce

Este projeto coleta e analisa avaliações de produtos em e-commerce, classificando automaticamente os sentimentos para auxiliar consumidores na tomada de decisão. Os dados são extraídos da plataforma Kabum via **web scraping**, processados com modelos de linguagem pré-treinados e disponibilizados por meio de uma **API REST**, com visualização em interface web em **React.js**.

## Pré-requisitos

Antes de começar, você precisa ter instalado:

- Python 3.9 ou superior
- **Poetry** (Gerenciador de dependências)
- MongoDB
- Navegador Chrome

## Instalação das Dependências

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
* Se for necessário ativar o ambiente virtual manualmente, utilize: `poetry shell`.