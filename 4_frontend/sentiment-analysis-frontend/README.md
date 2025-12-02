# Frontend - Review Sentimentum

Este é o frontend do projeto de Análise de Sentimentos para E-commerce. Desenvolvido com **Next.js**, **React**, **Shadcn** e **Tailwind CSS**, ele oferece uma interface de usuário moderna e responsiva para interagir com a API de produtos, permitindo que os usuários explorem, busquem e analisem as avaliações de produtos de informática de forma intuitiva.

A aplicação consome os dados da API REST (Backend) para exibir informações detalhadas dos produtos, estatísticas de sentimento e os comentários individuais classificados por um modelo de IA.

## Funcionalidades

- **Página Inicial Dinâmica**: Permite a busca direta por código, nome ou link do produto, além da exploração de produtos por categorias.
- **Busca Inteligente**: Redireciona automaticamente para a página de detalhes se um código ou link de produto é inserido, ou para uma página de resultados de busca para termos textuais.
- **Visualização de Produtos**:
    - **Página de Detalhes**: Exibe informações completas de um produto, incluindo dados técnicos, link para a loja, estatísticas de sentimento (gráficos de pizza e barras) e uma lista detalhada de todas as avaliações coletadas.
    - **Cards de Produto**: Componentes reutilizáveis que exibem um resumo do produto nas páginas de listagem.
- **Exploração por Categorias**: Um menu de navegação hierárquico e interativo que permite ao usuário explorar produtos por departamento, categoria e subcategoria.
- **Paginação**: Controle de paginação para navegar facilmente por grandes volumes de resultados de busca e listagens de categoria.
- **Design Responsivo**: Interface adaptada para uma ótima experiência em desktops, tablets e dispositivos móveis.
- **Página "Sobre"**: Uma página dedicada que explica o propósito, o desafio e a arquitetura tecnológica do projeto.

## Estrutura de Arquivos

A estrutura do projeto segue as convenções do App Router do Next.js.

```
sentiment-analysis-frontend/
│
├── public/                 # Arquivos estáticos (imagens, ícones).
│
├── src/
│   ├── app/
│   │   ├── (rotas)/        # Pastas que definem as rotas da aplicação (ex: /produto/[id], /busca).
│   │   ├── actions/        # Server Actions para buscar dados da API.
│   │   ├── globals.css     # Estilos globais.
│   │   └── layout.tsx      # Layout principal da aplicação.
│   │
│   ├── components/
│   │   ├── ui/             # Componentes de UI base (shadcn/ui).
│   │   ├── header/         # Componente de cabeçalho.
│   │   ├── produto/        # Componentes específicos para a exibição de produtos.
│   │   └── ...             # Outros componentes reutilizáveis.
│   │
│   ├── lib/
│   │   └── utils.ts        # Funções utilitárias.
│   │
│   └── types/
│       └── produtos.ts     # Tipagens TypeScript para os dados de produtos.
│
├── package.json            # Dependências e scripts do projeto.
└── next.config.ts          # Configurações do Next.js.
```

## Bibliotecas Principais

- **Next.js**: Framework React para renderização no servidor e geração de sites estáticos.
- **React**: Biblioteca para construção de interfaces de usuário.
- **Tailwind CSS**: Framework de CSS utility-first para estilização.
- **shadcn/ui**: Coleção de componentes de UI reutilizáveis e acessíveis.
- **Lucide React**: Biblioteca de ícones.
- **Recharts**: Biblioteca para a criação de gráficos (usada nas estatísticas de sentimento).
- **ESLint**: Para linting e manutenção da qualidade do código.

## Pré-requisitos

- Node.js (versão 20 ou superior)
- npm ou yarn
- O **Backend (API)** do projeto deve estar em execução e acessível pela rede.

## Instalação

1.  Navegue até o diretório **raiz** do projeto.

2.  Verifique o arquivo `README.md` na pasta raiz para confirmar as dependências e requisitos de instalação.

## Instruções de Uso

1.  Siga as instruções no arquivo `README.md` no diretório **raiz** para os comandos de execução.

2.  **Abra seu navegador** e acesse a aplicação:
    [http://localhost:3000](http://localhost:3000)

