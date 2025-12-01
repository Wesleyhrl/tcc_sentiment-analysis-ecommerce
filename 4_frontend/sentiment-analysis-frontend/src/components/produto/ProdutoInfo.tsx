'use client'

import type { ProdutoInfo } from '@/types/produtos'
import { Card, CardContent } from '@/components/ui/card'

export default function ProdutoInfo({ produto }: { produto: ProdutoInfo }) {
  
  // Componente interno simples para as linhas de dados
  const InfoItem = ({ label, value }: { label: string, value: string | number }) => (
    <div className="flex justify-between items-center py-2 border-b border-border/50 last:border-0">
      <span className="text-sm font-medium text-muted-foreground">{label}</span>
      <span className="text-sm font-semibold text-foreground text-right">{value}</span>
    </div>
  )

  return (
    <Card className="border-none shadow-none bg-transparent">
      <CardContent className="p-0">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Coluna 1: Dados Técnicos */}
          <div className="flex flex-col">
            <InfoItem label="Marca" value={produto.marca} />
            <InfoItem label="Modelo" value={produto.modelo} />
            <InfoItem label="Loja" value={produto.loja} />
            <InfoItem label="Código" value={produto.codigo} />
            <InfoItem label="Localização" value={produto.localizacao} />
            <InfoItem 
              label="Data de extração" 
              value={new Date(produto.data_extracao).toLocaleDateString('pt-BR')} 
            />
          </div>

          {/* Coluna 2: Descrição */}
          <div className="flex flex-col h-full">
            <h4 className="text-sm font-semibold text-foreground mb-3">Descrição</h4>
            <div className="bg-muted/30 rounded-md p-4 h-full border border-border/40">
              <p className="text-sm text-muted-foreground leading-relaxed text-justify">
                {produto.descricao}
              </p>
            </div>
          </div>

        </div>
      </CardContent>
    </Card>
  )
}