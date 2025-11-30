// Interfaces para as avaliações
export interface Sentimento {
  label: 'positive' | 'negative' | 'neutral';
  score: number;
}

export interface Avaliacao {
  id: number;
  pagina: number;
  autor: string;
  nota: string;
  data: string;
  titulo: string;
  comentario: string;
  sentimento: Sentimento;
}

// Interface para o produto
export interface ProdutoInfo {
  titulo: string;
  localizacao: string;
  codigo: string;
  loja: string;
  descricao: string;
  marca: string;
  modelo: string;
  classificacao: number;
  total_avaliacoes_coletadas: number;
  url: string;
  data_extracao: string;
}

// Interfaces para as estatísticas
export interface EstatisticasSentimento {
  quantidade: number;
  percentual: number;
  media_confianca_ia: number;
}

export interface EstatisticasSentimentos {
  positive: EstatisticasSentimento;
  negative: EstatisticasSentimento;
  neutral: EstatisticasSentimento;
}

export interface Estatisticas {
  total_avaliacoes: number;
  media_nota: number;
  media_confianca_global_ia: number;
  sentimento_predominante: 'positive' | 'negative' | 'neutral';
  assimiliacao_nota_sentimento: number;
  estatisticas_sentimentos: EstatisticasSentimentos;
}

export interface ProdutoDataInfo {
  _id: string;
  produto: ProdutoInfo
}

// Interface principal para a resposta da API
export default interface ProdutoData {
  _id: string;
  avaliacoes: Avaliacao[];
  produto: ProdutoInfo;
  estatisticas: Estatisticas;
}