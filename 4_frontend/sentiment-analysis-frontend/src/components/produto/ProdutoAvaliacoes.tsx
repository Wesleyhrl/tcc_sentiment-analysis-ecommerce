'use client'

import { Avaliacao } from '@/types/produtos'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"

import { useState } from 'react'

export default function ProdutoAvaliacoes({ avaliacoes }: { avaliacoes: Avaliacao[] }) {

  const [filter, setFilter] = useState<'all' | 'positive' | 'neutral' | 'negative'>('all')

  const filteredAvaliacoes = filter === 'all' ? avaliacoes : avaliacoes.filter(a => a.sentimento.label === filter)

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold">Avaliações {filteredAvaliacoes.length}</h3>
      <ButtonGroup>
        <Button className='bg-black' onClick={() => setFilter('all')}>Todas</Button>
        <Button className='bg-positive hover:bg-green-800' onClick={() => setFilter('positive')}  >Positivas</Button>
        <Button className='bg-neutral hover:bg-gray-700' onClick={() => setFilter('neutral')} >Neutras</Button>
        <Button className='bg-negative hover:bg-red-800' onClick={() => setFilter('negative')} >Negativas</Button>
      </ButtonGroup>
      <div className="grid gap-4">
        {filteredAvaliacoes.map((a) => (
          <Card key={a.id}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold">{a.titulo}</h4>
                <Badge
                  className={
                    a.sentimento.label === 'positive'
                      ? 'bg-positive'
                      : a.sentimento.label === 'negative'
                        ? 'bg-negative'
                        : 'bg-neutral'
                  }
                >
                  {a.sentimento.label}
                </Badge>
              </div>
              <p className="text-sm text-gray-600 mb-2">por {a.autor} — {a.data}</p>
              <p className="mb-2">{a.comentario}</p>
              <p className="text-sm text-gray-500">Nota: {a.nota}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
