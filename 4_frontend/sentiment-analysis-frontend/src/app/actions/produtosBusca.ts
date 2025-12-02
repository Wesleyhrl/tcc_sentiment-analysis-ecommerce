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

export async function fetchProdutosBusca(
    titulo: string, 
    page: number = 1, 
    pageSize: number = 50,
    ordem: string = 'relevancia'
): Promise<ProdutoBuscaResponse | null> {
  try {
    const params = new URLSearchParams({
      titulo: titulo,
      page: page.toString(),
      page_size: pageSize.toString(),
      ordem: ordem,
    });

    const API_KEY = process.env.API_KEY;

    if (!API_KEY) {
      throw new Error("ERRO: API_KEY não definida no .env");
    }

    const response = await fetch(`${API_BASE_URL}/produtos/buscar/?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
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