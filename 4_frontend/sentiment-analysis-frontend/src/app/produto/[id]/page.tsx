import ProdutoData from '@/types/produtos'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Card, CardContent } from '@/components/ui/card'
import ProdutoInfo from '@/components/produto/ProdutoInfo'
import ProdutoEstatisticas from '@/components/produto/ProdutoEstatisticas'
import ProdutoAvaliacoes from '@/components/produto/ProdutoAvaliacoes'

export interface ProdutoRouteParams {
  id: string
}

export default async function Produto({ params }: { params: Promise<ProdutoRouteParams> }) {
  const API_BASE_URL = process.env.API_BASE_URL
  const { id: productId } = await params
  const response = await fetch(`${API_BASE_URL}/produtos/${productId}`, { cache: 'no-store' })
  const productData: ProdutoData = await response.json()

  return (
    <div className="container mx-auto py-8 space-y-6">
      <h1 className="text-3xl font-bold tracking-tight mb-6">{productData.produto.titulo}</h1>
      <div className="mb-6 p-2">
        <a
          href={productData.produto.url}
          target="_blank"
          rel="noopener noreferrer"
          className=" text-xl font-semibold text-blue-400 border-b-2 
          border-blue-400 pb-1 transition duration-150 ease-in-out hover:text-blue-900  hover:border-blue-900">
          Ver produto na KaBuM!
        </a>
      </div>

      {/* Accordion com dados do produto */}
      <Accordion type="single" collapsible className="bg-white p-4 rounded-md shadow-md mb-6">
        <AccordionItem value="info">
          <AccordionTrigger className="text-lg font-medium">Informações do Produto</AccordionTrigger>
          <AccordionContent>
            <ProdutoInfo produto={productData.produto} />
          </AccordionContent>
        </AccordionItem>
      </Accordion>

      {/* Estatísticas e avaliações */}
      <Card className="p-4">
        <CardContent>
          <ProdutoEstatisticas estatisticas={productData.estatisticas} />
        </CardContent>
      </Card>

      <ProdutoAvaliacoes avaliacoes={productData.avaliacoes} />
    </div>
  )
}
