'use server';

interface CategoryItem {
  nome_exibicao: string;
  caminho_completo: string;
}

export async function fetchNavigation(filtro: string = ''): Promise<CategoryItem[]> {
  try {
    // Substitua pela URL correta da sua API Python se estiver em Docker ou outra porta
    const apiUrl = `http://127.0.0.1:8000/produtos/navegacao/?filtro=${filtro}`;
    
    const response = await fetch(apiUrl, {
      cache: 'no-store', // Garante dados sempre frescos
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Falha ao buscar categorias');
    }

    return await response.json();
  } catch (error) {
    console.error('Erro na navegação:', error);
    return [];
  }
}