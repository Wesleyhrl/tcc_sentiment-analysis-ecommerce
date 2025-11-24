'use client';

import { useState, useEffect } from 'react';
import { ArrowLeftIcon, Loader2 } from 'lucide-react'; // Adicionei Loader2 para loading state
import { fetchNavigation } from '@/app/actions/navigation';
import { Button } from '@/components/ui/button';
import { ButtonGroup } from '@/components/ui/button-group'; // Certifique-se que este componente existe no seu projeto
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Spinner } from '@/components/ui/spinner';

interface CategoryItem {
  nome_exibicao: string;
  caminho_completo: string;
}

export default function CategoryMenu() {
  const [items, setItems] = useState<CategoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [history, setHistory] = useState<string[]>([]);

  // Função para carregar dados
  const loadCategories = async (filtro: string = '') => {
    setLoading(true);
    try {
      const data = await fetchNavigation(filtro);
      setItems(data);
    } catch (error) {
      console.error("Erro ao carregar categorias:", error);
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  // Carrega a raiz (Nível 1) ao iniciar
  useEffect(() => {
    loadCategories();
  }, []);

  // Ao clicar em uma categoria
  const handleNavigate = (caminho: string) => {
    setHistory([...history, caminho]);
    loadCategories(caminho);
  };

  // Ao clicar em "Voltar"
  const handleBack = () => {
    const newHistory = [...history];
    newHistory.pop(); // Remove o atual
    setHistory(newHistory);
    
    // O filtro para carregar é o último que sobrou, ou vazio (raiz)
    const prevFilter = newHistory.length > 0 ? newHistory[newHistory.length - 1] : '';
    loadCategories(prevFilter);
  };

  return (
    <ScrollArea type="auto" className="w-full pb-4 whitespace-nowrap">
      <div className="w-full flex justify-center">
        <ButtonGroup>
          
          {/* Grupo do Botão Voltar */}
          {history.length > 0 && (
            <ButtonGroup>
              <Button
                className='text-lg border-blue-400 text-blue-400 hover:bg-blue-400 
                hover:text-white active:bg-blue-400 active:text-white  transition duration-600 cursor-pointer' 
                variant="outline" 
                size="icon" 
                onClick={handleBack}
                disabled={loading}
                aria-label="Voltar"
                title="Voltar nível"
              >
                <ArrowLeftIcon className="h-4 w-4 stroke-4"/>
              </Button>
            </ButtonGroup>
          )}

          {/* Grupo dos Itens de Categoria */}
          <ButtonGroup>
            {loading ? (
              <Button variant="ghost" disabled className="cursor-wait">
                <Spinner className='mr-1 size-7 stroke-3'/>
                Carregando...
              </Button>
            ) : items.length > 0 ? (
              items.map((item) => (
                <Button
                  key={item.caminho_completo}
                  variant="outline"
                  onClick={() => handleNavigate(item.caminho_completo)}
                  className="capitalize  text-lg border-blue-400 text-blue-400 hover:bg-blue-400 
                  hover:text-white active:bg-blue-400 active:text-white  transition duration-600 cursor-pointer"
                >
                  {item.nome_exibicao.replace(/-/g, ' ')}
                </Button>
              ))
            ) : (
              <Button variant="ghost" disabled>
                Nenhuma subcategoria
              </Button>
            )}
          </ButtonGroup>

        </ButtonGroup>
      </div>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  );
}