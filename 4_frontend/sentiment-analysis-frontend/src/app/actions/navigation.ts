'use server';

interface CategoryItem {
  nome_exibicao: string;
  caminho_completo: string;
}

export async function fetchNavigation(filtro: string = ''): Promise<CategoryItem[]> {
  try {
    const API_BASE_URL = process.env.API_BASE_URL || 'http://127.0.0.1:8000';
    const apiUrl = `${API_BASE_URL}/produtos/navegacao/?filtro=${filtro}`;
    
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error('Falha ao buscar categorias');
    }

    return await response.json();
  } catch (error) {
    console.error('Erro na navegação:', error);
    return [];
  }
}