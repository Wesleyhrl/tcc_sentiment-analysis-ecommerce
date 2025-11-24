'use client';

import { Search } from 'lucide-react';
import { useFormStatus } from 'react-dom';

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { Spinner } from '../ui/spinner';

interface InputSearchProps {
  searchAction: (formData: FormData) => void;
}

export default function InputSearch({ searchAction }: InputSearchProps) {
  const { pending } = useFormStatus();
  return (
    <form action={searchAction} className="w-full max-w-lg">
      <InputGroup className='py-5 bg-white'>
        <InputGroupInput
          name="search"
          placeholder="Digite 'Código', 'Nome' ou 'Link' do produto"
          required
          className="!text-base borde"
        />

        <InputGroupAddon align="inline-end">
          <InputGroupButton className='bg-primary-blue text-text-secondary text-base py-3.5 cursor-pointer 
          hover:bg-blue-700 transition-colors font-bold'
            variant="secondary" type="submit" disabled={pending}>
            {pending ? (
              <Spinner className="mr-2" strokeWidth={3.5} />
            ) : (
              <Search className="mr-2" strokeWidth={3.5} />
            )}
            {pending ? 'Buscando...' : 'Buscar'}
          </InputGroupButton>
        </InputGroupAddon>
      </InputGroup>
    </form>
  );
}