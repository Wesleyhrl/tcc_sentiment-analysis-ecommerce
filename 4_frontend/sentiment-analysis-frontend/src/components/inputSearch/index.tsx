
import { Search } from 'lucide-react';

interface InputSearchProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: () => void;
}

export default function InputSearch({ value, onChange, onSearch }: InputSearchProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch();
  };

  return (
    <form onSubmit={handleSubmit} className="flex w-full max-w-lg items-center">
      <div className="relative w-full">
        <label htmlFor="search" className="sr-only">
          Buscar
        </label>
        <input
          id="search"
          type="search"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Digite 'Código' ou 'Nome' ou 'Link' do produto"
          className="w-full rounded-tl-lg rounded-bl-lg border border-gray-300 bg-gray-50 py-2.5 pl-10 pr-4 text-sm 
          text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white 
          dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
        />
        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <Search className="h-5 w-5 text-gray-500 dark:text-gray-400" />
        </div>
      </div>
      <button
        type="submit"
        className="inline-flex items-center rounded-tr-lg rounded-br-lg border border-blue-700 bg-blue-700 px-4 py-2.5 text-sm 
        font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 
        dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <Search className="mr-2 h-4 w-4" /> Buscar
      </button>
    </form>
  );
}