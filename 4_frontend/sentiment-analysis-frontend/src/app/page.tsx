// app/page.tsx
'use client';

import { useState } from 'react';
import SearchInput from './../components/inputSearch/index';

import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [searchValue, setSearchValue] = useState('');
  const [submittedValue, setSubmittedValue] = useState('');

  const handleSearch = () => {
    setSubmittedValue(searchValue);
    if(/^\d+$/.test(searchValue)){
      router.push(`/produto/${searchValue}`);
    }
    
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex flex-col items-center justify-center bg-background p-4">
      <SearchInput 
        value={searchValue}
        onChange={setSearchValue}
        onSearch={handleSearch}
      />
      
      {/* Área para mostrar o valor do input */}
      {submittedValue && (
        <div className="mt-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md max-w-lg w-full">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Valor pesquisado:
          </h2>
          <p className="text-gray-700 dark:text-gray-300 break-words">
            {submittedValue}
          </p>
        </div>
      )}
    </div>
  );
}