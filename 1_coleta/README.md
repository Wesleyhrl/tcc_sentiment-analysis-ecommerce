# Módulo de Coleta de Dados

Este módulo é a primeira etapa do projeto de Análise de Sentimentos. Sua principal responsabilidade é realizar a coleta de dados brutos de produtos e suas respectivas avaliações a partir de sitemaps de sites de e-commerce. O processo é automatizado para extrair informações detalhadas das páginas de produtos, incluindo descrições, especificações técnicas, e, crucialmente, todos os comentários e notas deixadas por usuários.

Os dados coletados são persistidos em um banco de dados MongoDB, servindo como a fonte primária de informação para as etapas subsequentes de análise e processamento. O scraper foi projetado para ser resiliente, com mecanismos de retentativa e capacidade de resumir a coleta de onde parou, evitando a re-extração de dados já processados.

## Funcionalidades

- **Processamento de Sitemaps:** Extrai URLs de sitemaps XML para identificar páginas de produtos.
- **Scraping de Produtos:** Navega até as páginas de produtos e extrai:
  - Informações do produto (título, código, categoria, descrição, detalhes técnicos).
  - Classificação geral do produto.
  - Todas as avaliações de usuários (autor, nota, data, título, comentário).
- **Paginação de Avaliações:** Navega automaticamente por todas as páginas de comentários para garantir a coleta completa.
- **Persistência de Dados:** Salva os dados estruturados em um banco de dados MongoDB.
- **Resiliência e Continuidade:** Verifica quais produtos já foram coletados e ignora-os, permitindo que a execução seja retomada sem duplicidade.
- **Mecanismo de Retentativa:** Tenta extrair os dados de um produto múltiplas vezes em caso de falha antes de desistir.
- **Logging Detalhado:** Registra todo o processo, incluindo sucessos, avisos e erros, para facilitar o monitoramento e a depuração.

## Estrutura de Arquivos

```
1_coleta/
│
├─── main.py                # Ponto de entrada que orquestra todo o processo de coleta.
├─── scraping.py            # Contém a lógica de scraping usando Selenium para extrair dados das páginas.
├─── sitemap.py             # Responsável por baixar e processar os sitemaps XML.
├─── resume.py              # Gerencia estatísticas e o estado da execução para permitir a continuidade.
├─── logger_config.py       # Configuração do sistema de logging para registro de eventos.
├─── robots.txt             # (Informativo) Regras de scraping para o domínio alvo.
└─── logs/                  # Diretório onde os arquivos de log são armazenados.
```

## Bibliotecas Utilizadas

- **requests:** Para realizar requisições HTTP e baixar os sitemaps.
- **lxml:** Para processar e extrair dados dos arquivos XML dos sitemaps.
- **selenium:** Para automação do navegador (scraping dinâmico) e extração de conteúdo de páginas renderizadas com JavaScript.
- **pymongo:** Para conectar e interagir com o banco de dados MongoDB, onde os dados são armazenados.

## Pré-requisitos

- Python 3.13+
- Poetry para gerenciamento de dependências.
- Uma instância do MongoDB em execução e acessível.
- Google Chrome instalado (o Selenium utilizará o `chromedriver`).

## Instalação

1.  Navegue até o diretório **raiz** do projeto.

2.  Verifique o arquivo `README.md` na pasta raiz para confirmar as dependências e requisitos de instalação.

## Instruções de Uso

1.  Siga as instruções no arquivo `README.md` no diretório **raiz** para os comandos de execução.

2.  **Acompanhe o Progresso:**
    O progresso da execução será exibido no console. Logs detalhados serão salvos na pasta `1_coleta/logs/`, permitindo uma análise mais aprofundada em caso de erros.

3.  **Verifique os Dados:**
    Após a execução, os dados estarão disponíveis no MongoDB, no banco de dados `kabum_scraping`, dentro das coleções `sitemaps` e `produtos`.
