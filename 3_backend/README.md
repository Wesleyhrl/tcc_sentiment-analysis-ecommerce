# Backend - API de Produtos e Análise de Sentimentos

## Descrição

Esta é a API central do projeto de Análise de Sentimentos para E-commerce. Construída com FastAPI, ela serve como a ponte entre o banco de dados MongoDB (populado pelos scripts de coleta e análise) e a aplicação frontend.

A API oferece endpoints para consultar informações detalhadas de produtos, navegar pela estrutura de categorias, e realizar buscas textuais com ordenação avançada.

## Funcionalidades

- **Consulta de Produtos**: Obtenha informações completas de um produto, incluindo suas estatísticas de sentimento e avaliações, através de um ID.
- **Navegação por Categorias**: Explore a árvore de categorias de produtos de forma hierárquica, desde os departamentos raiz até as subcategorias mais específicas.
- **Busca Avançada**: Realize buscas textuais por nome de produto com suporte a paginação e ordenação por relevância ou popularidade (número de coletas).
- **Listagem por Localização**: Liste todos os produtos que pertencem a uma determinada categoria ou subcategoria.
- **Estrutura Assíncrona**: Totalmente construída sobre `async/await`, garantindo alta performance e escalabilidade.

## Estrutura de Arquivos

```
3_backend/
│
├── core/
│   ├── config.py       # Carrega variáveis de ambiente (URL do DB).
│   └── database.py     # Gerencia a conexão com o MongoDB.
│
├── models/
│   ├── navegacao_model.py  # Modelos de dados para a navegação.
│   ├── pagination_model.py # Modelo de dados para respostas paginadas.
│   └── produto_model.py    # Modelos Pydantic para os produtos.
│
├── routers/
│   └── produto_router.py # Define os endpoints da API relacionados a produtos.
│
├── services/
│   └── produto_service.py  # Contém a lógica de negócio para interagir com o DB.
│
├── utils/
│   └── localizacao_utils.py # Funções utilitárias para manipulação de URLs.
│
└── main.py             # Ponto de entrada da aplicação FastAPI.
```

## Bibliotecas Principais

- **FastAPI**: Framework web para a construção da API.
- **Pydantic**: Para validação e modelagem de dados.
- **Motor**: Driver assíncrono para interagir com o MongoDB.
- **Python-dotenv**: Para gerenciamento de variáveis de ambiente.

## Pré-requisitos

- Python 3.10+
- Poetry para gerenciamento de dependências.
- Uma instância do MongoDB em execução e acessível.
- As coleções do banco de dados (`produtos`) devem ter sido populadas pelos scripts das etapas `1_coleta` e `2_analise`.

## Instalação

1.  Navegue até o diretório **raiz** do projeto.

2.  Verifique o arquivo `README.md` na pasta raiz para confirmar as dependências e requisitos de instalação.

## Instruções de Uso

1.  Siga as instruções no arquivo `README.md` no diretório **raiz** para os comandos de execução.

2.  **Acesse a documentação interativa (Swagger UI)** para testar os endpoints em seu navegador:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


