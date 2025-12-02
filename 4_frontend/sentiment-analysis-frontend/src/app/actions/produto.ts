'use server'

import ProdutoData from '@/types/produtos'

const API_BASE_URL = process.env.API_BASE_URL || 'http://127.0.0.1:8000';

export async function fetchProduto(id: string): Promise<ProdutoData | null> {
  try {
    const API_KEY = process.env.API_KEY;

    if (!API_KEY) {
      throw new Error("ERRO: API_KEY não definida no .env");
    }

    const response = await fetch(`${API_BASE_URL}/produtos/${id}`, { 
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY,
      },
      cache: 'no-store' 
    })
    
    if (!response.ok) return null
    
    return await response.json()
  } catch (error) {
    console.error('Erro ao buscar produto:', error)
    return null
  }
}