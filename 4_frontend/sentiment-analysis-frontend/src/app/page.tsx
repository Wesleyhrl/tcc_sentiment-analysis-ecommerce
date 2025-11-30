import { redirect } from 'next/navigation';
import SearchInput from '../components/inputSearch/index';
import CategoryMenu from '../components/categoryMenu/index';
import {  Logs  } from 'lucide-react';
import ProdutoExplorer from '@/components/produto/ProdutoExplorer';

async function searchProducts(formData: FormData) {
  'use server';
  const searchValue = formData.get('search') as string;

  if (/^\d+$/.test(searchValue)) {
    redirect(`/produto/${searchValue}`);
  }

  const kabumLinkRegex = /https?:\/\/(www\.)?kabum\.com\.br\/produto\/(\d+)/;
  const match = searchValue.match(kabumLinkRegex);

  if (match && match[2]) {
    const extractedId = match[2];
    redirect(`/produto/${extractedId}`);
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