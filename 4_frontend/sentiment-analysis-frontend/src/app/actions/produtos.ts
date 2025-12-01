'use server';

import { ProdutoDataInfo } from '@/types/produtos';

export interface ProdutoListaResponse {
  items: ProdutoDataInfo[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export async function fetchProdutosLista(
  filtro: string = '', 
  page: number = 1, 
  pageSize: number = 12,
  ordem: string = 'relevancia'
): Promise<ProdutoListaResponse | null> {
  try {
    const API_BASE_URL = process.env.API_BASE_URL;
    const apiUrl = `${API_BASE_URL}/produtos/listar/localizacao/?filtro=${filtro}&page=${page}&page_size=${pageSize}&ordem=${ordem}`;
    
    const response = await fetch(apiUrl, {
        cache: "force-cache",
      next: { revalidate: 60 }, // Cache de 60 segundos
    });

    if (!response.ok) {
      throw new Error('Falha ao buscar produtos');
    }

    return await response.json();
  } catch (error) {
    console.error('Erro na listagem de produtos:', error);
    return null;
  }
}