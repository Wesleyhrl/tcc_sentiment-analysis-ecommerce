'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ProdutoCard from '@/components/produto/ProdutoCard'; // Ajuste o caminho conforme sua estrutura
import PaginationControl from '@/components/pagination'; // Ajuste o caminho
import { Spinner } from '@/components/ui/spinner'; // Ajuste o caminho
import SearchInput from '@/components/inputSearch/index'; // Opcional: Para permitir nova busca na mesma tela
import { ProdutoBuscaResponse, fetchProdutosBusca } from '@/app/actions/produtosBusca';

function SearchContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    
    // Pega o termo 'q' da URL (ex: /busca?q=iphone)
    const query = searchParams.get('q') || '';
    
    const [data, setData] = useState<ProdutoBuscaResponse | null>(null);
    const [loading, setLoading] = useState(false);
    
    // Estado local da página. Se a query mudar, voltamos para página 1 automaticamente.
    const [currentPage, setCurrentPage] = useState(1);

    // Efeito para resetar a página quando o termo de busca mudar
    useEffect(() => {
        setCurrentPage(1);
    }, [query]);

    // Função principal de busca
    const loadSearchResults = async () => {
        if (!query.trim()) {
            setData(null);
            return;
        }

        setLoading(true);
        try {
            const result = await fetchProdutosBusca(query, currentPage);
            setData(result);
        } catch (error) {
            console.error("Falha na busca", error);
        } finally {
            setLoading(false);
        }
    };

    // Dispara a busca quando a query (URL) ou a paginação mudar
    useEffect(() => {
        loadSearchResults();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [query, currentPage]);

    // Handler para paginação
    const handlePageChange = (page: number) => {
        setCurrentPage(page);
        // Opcional: Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Reutilizando a lógica de redirecionamento para o SearchInput interno (se houver)
    const handleNewSearch = async (formData: FormData) => {
        const searchValue = formData.get('search') as string;
        if (searchValue.trim() !== '') {
            router.push(`/busca?q=${encodeURIComponent(searchValue.trim())}`);
        }
    };

    return (
        <div className="min-h-[calc(100vh-64px)] flex flex-col items-center bg-background p-4 w-full">
            
            {/* Opcional: Input de busca no topo para refazer a pesquisa */}
            <div className="mb-8 w-full flex justify-center">
                 {/* Precisamos passar uma server action ou adaptar o SearchInput. 
                     Aqui estou assumindo que ele aceita prop ou funciona client-side.
                     Se ele exigir Server Action, use a mesma da Home. */}
                 {/* <SearchInput searchAction={...} /> */} 
                 
                 {/* Título da Busca */}
                 <h1 className="text-2xl font-bold text-[#193f76]">
                    Resultados para: <span className="text-blue-500 italic">"{query}"</span>
                 </h1>
            </div>

            <div className="w-full max-w-[1400px]">
                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="flex flex-col items-center gap-2">
                            <Spinner className="size-10 text-[#193f76]" />
                            <span className="text-gray-500 text-sm">Buscando produtos...</span>
                        </div>
                    </div>
                ) : !data || data.items.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20 text-center">
                        <p className="text-gray-500 text-lg mb-2">
                            Nenhum produto encontrado para <strong>"{query}"</strong>.
                        </p>
                        <p className="text-sm text-gray-400">
                            Tente verificar a ortografia ou usar termos mais genéricos.
                        </p>
                    </div>
                ) : (
                    <>
                        <div className="flex flex-col sm:flex-row justify-between items-center mb-6 px-1 border-b pb-2 border-gray-200">
                            <h2 className="text-xl font-bold text-gray-700">
                                Produtos Encontrados
                            </h2>
                            <div className="mt-1 sm:mt-0 text-gray-500">
                                <span className="text-sm font-bold text-[#193f76]">
                                    {data.total}
                                </span> resultados
                            </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            {data.items.map((item) => (
                                <ProdutoCard key={item._id} data={item} />
                            ))}
                        </div>

                        <div className="mt-10 mb-10">
                            <PaginationControl
                                currentPage={data.page}
                                totalPages={data.pages}
                                onPageChange={handlePageChange}
                                isLoading={loading}
                            />
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}

// Necessário envolver em Suspense pois usamos useSearchParams
export default function BuscaPage() {
    return (
        <Suspense fallback={<div className="flex justify-center p-10"><Spinner /></div>}>
            <SearchContent />
        </Suspense>
    );
}