
import ProdutoData from '@/types/produtos';

export interface ProdutoRouteParams {
  id: string;
}


export default async function Produto({ params }: { params: Promise<ProdutoRouteParams> }) {
  const API_BASE_URL = process.env.API_BASE_URL;
  const { id: productId } = await params;
  const response = await fetch(`${API_BASE_URL}/produtos/${productId}`);
  const productData: ProdutoData = await response.json();
  
  console.log(productData);
  
  return (
    <div>
      <h1>Produto: {productId}</h1>
      <h2>{productData.produto.titulo}</h2>
      <p>Avaliações: {productData.estatisticas.total_avaliacoes}</p>
    </div>
  );
}