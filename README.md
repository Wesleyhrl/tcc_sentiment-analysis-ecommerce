# Sistema de Análise de Sentimentos para Avaliações de Produtos de E-commerce

Este projeto coleta e analisa avaliações de produtos em e-commerce, classificando automaticamente os sentimentos para auxiliar consumidores na tomada de decisão.   Os dados são extraídos da plataforma Kabum via **web scraping**, processados com modelos de linguagem pré-treinados e disponibilizados por meio de uma **API REST**, com visualização em interface web em **React.js**.

## Pré-requisitos

Antes de começar, você precisa ter instalado:

- Python 3.9 ou superior
- pip
- MongoDB
- Navegador Chrome

## Instalação das Dependências

É recomendado criar um ambiente virtual para o projeto, isolando as dependências:

1. Crie o ambiente virtual:

```bash
python -m venv venv
````

2. Ative o ambiente virtual:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux/Mac:**

```bash
source venv/bin/activate
```

3. Após ativar o `venv`, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Instalação do PyTorch

O PyTorch deve ser instalado de acordo com o hardware do seu computador (CPU ou GPU).

1. Acesse o site oficial do PyTorch: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)
2. Verifique se as opções são compatíveis para sistema/hardware.
3. Copie o comando gerado pelo site e execute no terminal. Por exemplo:

* Para GPU com (CUDA 12.9):

```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129
```

> Deve escolher a versão correta conforme seu hardware. Seguir o site oficial garante compatibilidade.

