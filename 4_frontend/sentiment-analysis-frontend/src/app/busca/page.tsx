'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ProdutoCard from '@/components/produto/ProdutoCard';
import PaginationControl from '@/components/pagination';
import { Spinner } from '@/components/ui/spinner';
import { ProdutoBuscaResponse, fetchProdutosBusca } from '@/app/actions/produtosBusca';

function SearchContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    
    const query = searchParams.get('q') || '';
    
    const [data, setData] = useState<ProdutoBuscaResponse | null>(null);
    const [loading, setLoading] = useState(false);
    
    const [currentPage, setCurrentPage] = useState(1);

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
    }, [query, currentPage]);

    // Handler para paginação
    const handlePageChange = (page: number) => {
        setCurrentPage(page);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <div className="min-h-[calc(100vh-64px)] flex flex-col items-center bg-background p-4 w-full">
            <div className="mb-8 w-full flex justify-center">
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