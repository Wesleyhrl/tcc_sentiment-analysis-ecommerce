'use server';
import { ProdutoDataInfo } from "@/types/produtos";


export interface ProdutoBuscaResponse {
  items: ProdutoDataInfo[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

const API_BASE_URL = process.env.API_BASE_URL || 'http://127.0.0.1:8000';

export async function fetchProdutosBusca(titulo: string, page: number = 1, pageSize: number = 50): Promise<ProdutoBuscaResponse | null> {
  try {
    const params = new URLSearchParams({
      titulo: titulo,
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    const response = await fetch(`${API_BASE_URL}/produtos/buscar/?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      console.error('Erro ao buscar produtos:', response.statusText);
      return null;
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro de conexão:', error);
    return null;
  }
}