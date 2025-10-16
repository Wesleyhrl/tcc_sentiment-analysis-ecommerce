
import { redirect } from 'next/navigation';
import SearchInput from '../components/inputSearch/index';

interface IdData{
  _id: string;
}

async function searchProducts(formData: FormData) {
  'use server';
  
  const searchValue = formData.get('search') as string;
  
  if (/^\d+$/.test(searchValue)) {
    redirect(`/produto/${searchValue}`);
  }

  const kabumLinkRegex = /https?:\/\/(www\.)?kabum\.com\.br\/produto\/(\d+)/;
  const match = searchValue.match(kabumLinkRegex);
  

  if(match){
      const API_BASE_URL = process.env.API_BASE_URL
      const response = await fetch(`${API_BASE_URL}/produtos/url/?url=${searchValue}`, { cache: 'no-store' })
      const data: IdData = await response.json()
      console.log(data._id)
      redirect(`/produto/${data._id}`);
  }

}

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center bg-background p-4">
      <SearchInput searchAction={searchProducts} />
    </div>
  );
}