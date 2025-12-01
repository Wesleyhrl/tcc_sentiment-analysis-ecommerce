import { redirect } from 'next/navigation';
import SearchInput from '../components/inputSearch/index';
import ProdutoExplorer from '@/components/produto/ProdutoExplorer';

async function searchProducts(formData: FormData) {
  'use server';
  const searchValue = formData.get('search') as string;
  //Redireciona se for um ID numérico puro
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
  //Redireciona para a página de busca com o termo pesquisado
  if (searchValue.trim() !== '') {
    redirect(`/busca?q=${encodeURIComponent(searchValue.trim())}`);
  }

}

export default async function Home() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center bg-background p-4">
      <SearchInput searchAction={searchProducts} />
      <ProdutoExplorer />
    </div>
  );
}