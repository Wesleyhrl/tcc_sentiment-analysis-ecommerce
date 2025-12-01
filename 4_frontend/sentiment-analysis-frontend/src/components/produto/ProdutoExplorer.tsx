'use client';

import { useState, useEffect } from 'react';
import { fetchProdutosLista, ProdutoListaResponse } from '@/app/actions/produtos';
import ProdutoCard from './ProdutoCard';
import PaginationControl from '../pagination';
import CategoryMenu from '../categoryMenu/index';
import { Spinner } from '@/components/ui/spinner';

export default function ProdutoExplorer() {
    const [filter, setFilter] = useState("");
    const [page, setPage] = useState(1);
    const [data, setData] = useState<ProdutoListaResponse | null>(null);
    const [loading, setLoading] = useState(false);

    const loadProducts = async () => {
        setLoading(true);
        if (filter == "") {
            setData(null);
        } else {
            const result = await fetchProdutosLista(filter, page);
            setData(result);
        }
        setLoading(false);
    };

    useEffect(() => {
        loadProducts()  
    }, [filter, page]);

    const handleCategoryChange = (newFilter: string) => {
        setFilter(newFilter);
        setPage(1);
    };

    const getCategoryTitle = (path: string) => {
        if (!path) return "";
        const lastPart = path.split('/').pop();
        return lastPart?.replace(/-/g, ' ') || "";
    }

    return (
        <div className="w-full">
            {/* Menu de Categorias */}
            <div className="w-full mb-6 mt-10">
                <CategoryMenu onCategorySelect={handleCategoryChange} />
            </div>

            {/* Área de Listagem */}
            <div className="min-h-[400px]">
                {filter == "" ? (
                    <div className="text-center text-gray-500 py-10">
                        Selecione uma categoria para visualizar os produtos.
                    </div>
                ) : loading ? (
                    <div className="flex justify-center items-center h-64">
                        <Spinner className="size-10 text-[#193f76]" />
                    </div>
                ) : !data || data.items.length === 0 ? (
                    <div className="text-center text-gray-500 py-10">
                        Nenhum produto encontrado nesta categoria.
                    </div>
                ) : (
                    <>
                        <div className="flex flex-col sm:flex-row justify-between items-center mb-6 px-1 border-b pb-2 border-gray-200">
                            <h2 className="text-xl sm:text-2xl font-bold text-slate-700 capitalize">
                                {getCategoryTitle(filter)}
                            </h2>
                            <div className="mt-1 sm:mt-0 text-gray-500">
                                <span className="text-sm font-bold ">{(data as any).total ?? data.items.length}</span> <span>produtos</span>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            {data.items.map((item) => (
                                <ProdutoCard key={item._id} data={item} />
                            ))}
                        </div>

                        <PaginationControl
                            currentPage={data.page}
                            totalPages={data.pages}
                            onPageChange={setPage}
                            isLoading={loading}
                        />
                    </>
                )}
            </div>
        </div>
    );
}