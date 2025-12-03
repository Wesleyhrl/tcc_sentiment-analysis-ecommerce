import { redirect } from 'next/navigation';
import SearchInput from '../components/inputSearch/index'; 
import ProdutoExplorer from '@/components/produto/ProdutoExplorer';

async function searchProducts(formData: FormData) {
  'use server';
  
  // Obtém o valor de forma segura e converte para string
  const rawSearch = formData.get('search');
  
  // Proteção contra valor nulo ou vazio
  if (!rawSearch) {
    return; // Não faz nada se não tiver dados
  }

  const searchValue = rawSearch.toString().trim();

  // Se após o trim estiver vazio, também retorna
  if (searchValue === '') {
      return; 
  }

  // Redireciona se for um ID numérico puro (ex: "12345")
  if (/^\d+$/.test(searchValue)) {
    redirect(`/produto/${searchValue}`);
  }

  // Redireciona se for um link de produto da Kabum
  const kabumLinkRegex = /https?:\/\/(www\.)?kabum\.com\.br\/produto\/(\d+)/;
  const match = searchValue.match(kabumLinkRegex);
  if (match && match[2]) {
    const extractedId = match[2];
    redirect(`/produto/${extractedId}`);
  }

  // Redireciona para a página de busca com o termo pesquisado
  redirect(`/busca?q=${encodeURIComponent(searchValue)}`);
}

export default async function Home() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center bg-background p-4">
      <SearchInput searchAction={searchProducts} />
      <ProdutoExplorer />
    </div>
  );
}