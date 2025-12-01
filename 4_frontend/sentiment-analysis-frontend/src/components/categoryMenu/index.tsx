'use client';

import { useState, useEffect } from 'react';
import { ArrowLeftIcon, Settings2 } from 'lucide-react';
import { fetchNavigation } from '@/app/actions/navigation';
import { Button } from '@/components/ui/button';
import { ButtonGroup } from '@/components/ui/button-group'; 
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Spinner } from '@/components/ui/spinner';

interface CategoryItem {
  nome_exibicao: string;
  caminho_completo: string;
}

interface CategoryMenuProps {
  onCategorySelect?: (filter: string) => void;
}

export default function CategoryMenu({ onCategorySelect }: CategoryMenuProps) {
  const [items, setItems] = useState<CategoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [history, setHistory] = useState<string[]>([]);

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

  useEffect(() => {
    loadCategories();
  }, []);

  const handleNavigate = (caminho: string) => {
    setHistory([...history, caminho]);
    loadCategories(caminho);
    if (onCategorySelect) onCategorySelect(caminho);
  };

  const handleBack = () => {
    const newHistory = [...history];
    newHistory.pop(); 
    setHistory(newHistory);
    
    const prevFilter = newHistory.length > 0 ? newHistory[newHistory.length - 1] : '';
    loadCategories(prevFilter);
    if (onCategorySelect) onCategorySelect(prevFilter);
  };

  return (
    // Container externo para centralizar tudo na tela
    <div className="w-full flex justify-start px-1">
      
      {/*Container inteligente: "w-fit" abraça o conteúdo, "max-w-full" impede que estoure a tela */}
      <div className="flex flex-col items-start w-fit max-w-full">
          
          {/*TÍTULO: Fica fora do ScrollArea, então não rola, mas está preso ao container dos botões */}
          <div className='flex items-center  gap-1'>
              <Settings2 className="w-6 h-6 text-slate-700" />
              <span className='text-xl sm:text-2xl font-bold mb-1 text-slate-700'>Categorias</span>
          </div>

          {/*SCROLL AREA: Apenas os botões rolam aqui dentro se passarem do limite */}
          <ScrollArea type="auto" className="w-full whitespace-nowrap px-1 pb-4">
            <ButtonGroup>
              
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
                      className="capitalize text-lg border-blue-400 text-blue-400 hover:bg-blue-400 
                      hover:text-white active:bg-blue-400 active:text-white transition duration-600 cursor-pointer"
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
            <ScrollBar orientation="horizontal" />
          </ScrollArea>

      </div>
    </div>
  );
}