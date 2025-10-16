'use client'

import { Star } from 'lucide-react';
import { Estatisticas } from '@/types/produtos'
import { Progress } from '@/components/ui/progress'
import { Card, CardContent } from '@/components/ui/card'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from 'recharts'

const COLORS = {
  positive: '#16a34a', // verde
  neutral: '#64748b',  // cinza
  negative: '#dc2626', // vermelho
}

export default function ProdutoEstatisticas({ estatisticas }: { estatisticas: Estatisticas }) {
  

  if (estatisticas.total_avaliacoes) {
    const { estatisticas_sentimentos } = estatisticas
    const sentimentosData = (['positive', 'neutral', 'negative'] as const).map((key) => ({
      name: key,
      percentual: estatisticas_sentimentos[key].percentual,
      media_confianca: estatisticas_sentimentos[key].media_confianca_ia,
    }))

      return (
    <div className="space-y-6">
      <h3 className="text-2xl font-semibold mb-2">Estatísticas de Sentimentos</h3>

      {/* Resumo geral */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <p><strong>Total de avaliações:</strong> {estatisticas.total_avaliacoes}</p>
          <p>
          <strong>Média de nota:</strong> {estatisticas.media_nota.toFixed(2)} 
          <Star className='inline pb-1' size={25} color="#ffea00" strokeWidth={3.5} absoluteStrokeWidth  />
          </p>
          <p><strong>Sentimento predominante:</strong>
            <span className="capitalize ml-1 font-medium text-primary">{estatisticas.sentimento_predominante}</span>
          </p>
          <p><strong>Assimilação nota/sentimento:</strong> {estatisticas.assimiliacao_nota_sentimento.toFixed(2)}</p>
          <p><strong>Média global de confiança IA:</strong> {estatisticas.media_confianca_global_ia.toFixed(2)}</p>
        </div>
      </div>

      {/* Gráficos */}
      <div className="grid md:grid-cols-2 gap-6 mt-6">
        {/* Gráfico de barras - Percentual */}
        <Card>
          <CardContent className="h-64 p-4">
            <h4 className="font-semibold mb-2 text-center">Distribuição de Sentimentos (%)</h4>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sentimentosData}>
                <XAxis dataKey="name" tickFormatter={(v) => v.charAt(0).toUpperCase() + v.slice(1)} />
                <YAxis />
                <Tooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
                <Bar dataKey="percentual" radius={[6, 6, 0, 0]}>
                  {sentimentosData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Gráfico de pizza - Confiança média IA */}
        <Card>
          <CardContent className="h-64 p-4">
            <h4 className="font-semibold mb-2 text-center">Confiança Média da IA</h4>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={sentimentosData}
                  dataKey="media_confianca"
                  nameKey="name"
                  outerRadius={80}
                  label={(entry) => `${entry.name}`}
                >
                  {sentimentosData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => value.toFixed(2)} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
  }else{
    return <div>Estatísticas de sentimentos indisponíveis.</div>
  }


}
