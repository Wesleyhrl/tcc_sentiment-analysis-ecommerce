
import { redirect } from 'next/navigation';
import SearchInput from '../components/inputSearch/index';

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
      console.log(`ID Extraído da URL: ${extractedId}`); // Opcional: para debug
      redirect(`/produto/${extractedId}`);
  }
}

export default async function Home() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center bg-background p-4">
      <SearchInput searchAction={searchProducts} />
    </div>
  );
}