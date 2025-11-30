import { Star, ChartNoAxesColumn, Barcode, Store, FileText } from 'lucide-react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ProdutoDataInfo } from '@/types/produtos';
import Link from 'next/link';

interface ProductCardProps {
  data: ProdutoDataInfo;
}

export default function ProdutoCard({ data }: ProductCardProps) {
  const { produto } = data;

  const prefixoParaRemover = "Vendido e entregue por: ";
  produto.loja = produto.loja.includes(prefixoParaRemover) ? produto.loja.replace(prefixoParaRemover, '') : produto.loja;


  return (
    <Link href={`/produto/${produto.codigo}`}>

      <Card className="flex flex-col h-full hover:shadow-lg transition-shadow duration-300">
        <CardHeader className="p-4 pb-2">
          <div className="flex justify-between items-start gap-2">
            <Badge className="mb-2 text-xs font-normal bg-text-primary">
              {produto.marca}
            </Badge>
          </div>
          <h3 className="font-semibold text-lg line-clamp-2 min-h-[40px] text-[#193f76]" title={produto.titulo}>
            {produto.titulo}
          </h3>
        </CardHeader>

        <CardContent className="p-4 pt-0 flex-grow">

          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Barcode className="w-4 h-4 text-gray-400" />
              <span className="truncate">{produto.codigo}</span>
            </div>
          </div>

          <div className="mt-1 space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Store className="w-4 h-4 text-gray-400" />
              <span className="truncate">{produto.loja}</span>
            </div>
          </div>

          <div className="mt-1 space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-gray-400" /> {/* Ícone para "Documentos/Reviews" */}
              <span className="truncate">
                {produto.total_avaliacoes_coletadas || 0} Avaliações Coletadas
              </span>
            </div>
          </div>

          <div className="mt-4 flex items-center gap-1">
            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            <span className="text-xs text-gray-500">
              {produto.classificacao} <span className='italic'>Classificação da Fonte</span>
            </span>
          </div>


        </CardContent>
      </Card>
    </Link>

  );
}