'use client';

import { useState, useEffect, useCallback } from 'react';
import { fetchProdutosLista, ProdutoListaResponse } from '@/app/actions/produtos';
import ProdutoCard from './ProdutoCard';
import PaginationControl from '../pagination'; 
import CategoryMenu from '../categoryMenu/index';
import { Spinner } from '@/components/ui/spinner';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

export default function ProdutoExplorer() {
    const [filter, setFilter] = useState("");
    const [page, setPage] = useState(1);
    const [sortOrder, setSortOrder] = useState("relevancia");
    const [data, setData] = useState<ProdutoListaResponse | null>(null);
    const [loading, setLoading] = useState(false);

    const loadProducts = useCallback(async () => {
        setLoading(true);
        if (filter === "") {
            setData(null);
        } else {
            try {
                const result = await fetchProdutosLista(filter, page, 12, sortOrder);
                setData(result);
            } catch (error) {
                console.error("Erro ao buscar produtos:", error);
            }
        }
        setLoading(false);
    }, [filter, page, sortOrder]);

    useEffect(() => {
        loadProducts();
    }, [loadProducts]);

    const handleCategoryChange = (newFilter: string) => {
        setFilter(newFilter);
        setPage(1);
    };

    const handleSortChange = (value: string) => {
        setSortOrder(value);
        setPage(1);
    };

    const getCategoryTitle = (path: string) => {
        if (!path) return "";
        const lastPart = path.split('/').pop();
        return lastPart?.replace(/-/g, ' ') || "";
    };

    return (
        <div className="w-full">
            <div className="w-full mb-6 mt-10">
                <CategoryMenu onCategorySelect={handleCategoryChange} />
            </div>

            <div className="min-h-[400px]">
                {filter === "" ? (
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
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 px-1 border-b pb-4 border-gray-200 gap-4">
                            <h2 className="text-xl sm:text-2xl font-bold text-slate-700 capitalize">
                                {getCategoryTitle(filter)}
                            </h2>

                            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 w-full md:w-auto">
                                <div className="flex items-center gap-2">
                                    <span className="text-sm text-gray-600 font-medium whitespace-nowrap">
                                        Ordenar por:
                                    </span>
                                    <Select value={sortOrder} onValueChange={handleSortChange}>
                                        <SelectTrigger className="w-[200px] bg-white">
                                            <SelectValue placeholder="Selecione a ordem" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="relevancia">Relevância</SelectItem>
                                            <SelectItem value="coletas">Mais Avaliados</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div className="text-gray-500 text-sm whitespace-nowrap">
                                    <span className="font-bold">{data?.total}</span> <span>produtos</span>
                                </div>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            {data?.items?.map((item) => (
                                <ProdutoCard key={item._id} data={item} />
                            ))}
                        </div>

                        {data && (
                            <PaginationControl
                                currentPage={data.page}
                                totalPages={data.pages}
                                onPageChange={setPage}
                                isLoading={loading}
                            />
                        )}
                    </>
                )}
            </div>
        </div>
    );
}