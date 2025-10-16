

import type { ProdutoInfo } from '@/types/produtos'

export default function ProdutoInfo({ produto }: { produto: ProdutoInfo }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      <div>
        <p><strong>Marca:</strong> {produto.marca}</p>
        <p><strong>Modelo:</strong> {produto.modelo}</p>
        <p><strong>Loja:</strong> {produto.loja}</p>
        <p><strong>Código:</strong> {produto.codigo}</p>
        <p><strong>Localização:</strong> {produto.localizacao}</p>
        <p><strong>Data de extração:</strong> {new Date(produto.data_extracao).toLocaleDateString()}</p>
      </div>
      <div>
        <p className="mt-3 text-gray-700"><strong>Descrição:</strong> {produto.descricao}</p>
      </div>
    </div>
  )
}
