'use client'

import { Star, Info, Activity, Brain, BarChart3, MessageCircle, ShieldCheck } from 'lucide-react';
import { Estatisticas } from '@/types/produtos'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine, Label
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
  
        {/*Modal*/}
        <div className="flex items-center gap-2 mb-2">
          <h3 className="text-2xl font-semibold">Estatísticas de Sentimentos</h3>
          
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-full h-8 w-8 text-muted-foreground hover:text-primary">
                <Info size={18} />
                <span className="sr-only">Entenda as estatísticas</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle className="text-xl flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-primary" />
                  Entendendo os Dados
                </DialogTitle>
                <DialogDescription>
                  Um guia rápido para interpretar as métricas de análise de sentimentos deste produto.
                </DialogDescription>
              </DialogHeader>

              <div className="grid gap-6 py-4">
                
                {/*Sentimento Predominante */}
                <div className="flex gap-4">
                  <div className="bg-blue-100 dark:bg-blue-900/30 p-2 rounded-lg h-fit">
                    <MessageCircle className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Sentimento Predominante</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      Indica qual emoção apareceu com mais frequência nos comentários. Se a maioria dos clientes elogiou, será "Positivo".
                    </p>
                  </div>
                </div>

                {/*Assimilação */}
                <div className="flex gap-4">
                  <div className="bg-amber-100 dark:bg-amber-900/30 p-2 rounded-lg h-fit">
                    <Activity className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Assimilação Nota/Sentimento</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      Mede a <strong>coerência</strong> do cliente. 
                      <br/>
                      • <strong>Alta (perto de 100%):</strong> A nota (estrelas) condiz com o texto escrito.
                      <br/>
                      • <strong>Baixa:</strong> Pode indicar incoerência (texto bom, nota baixa) ou erro de digitação do usuário.
                    </p>
                  </div>
                </div>

                {/*Confiança IA*/}
                <div className="flex gap-4">
                  <div className="bg-purple-100 dark:bg-purple-900/30 p-2 rounded-lg h-fit">
                    <Brain className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Confiança Média da IA</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      O quanto o nosso sistema de Inteligência Artificial tem certeza da sua análise. 
                      Valores acima da linha laranja (85%) indicam uma leitura confiável do contexto.
                    </p>
                  </div>
                </div>

                                 {/*Média Global de Confiança IA*/}
                 <div className="flex gap-4">
                  <div className="bg-emerald-100 dark:bg-emerald-900/30 p-2 rounded-lg h-fit">
                    <ShieldCheck className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Média Global de Confiança IA</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      A pontuação geral de certeza da IA para <strong>todos</strong> os comentários deste produto.
                      Uma média alta significa que os comentários foram muito claros e fáceis para a IA interpretar corretamente.
                    </p>
                  </div>
                </div>

              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/*Resumo geral*/}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-3 text-sm md:text-base">
            <div className="flex justify-between border-b pb-2">
              <span className="text-muted-foreground">Total de avaliações:</span>
              <span className="font-medium">{estatisticas.total_avaliacoes}</span>
            </div>
            
            <div className="flex justify-between border-b pb-2 items-center">
              <span className="text-muted-foreground">Média de nota:</span>
              <span className="font-medium flex items-center gap-1">
                {estatisticas.media_nota.toFixed(2)}
                <Star className='pb-0.5' size={18} fill="#ffea00" color="#eab308" />
              </span>
            </div>

            <div className="flex justify-between border-b pb-2">
              <span className="text-muted-foreground">Sentimento predominante:</span>
              <span className={`capitalize font-bold px-2 py-0.5 rounded text-xs items-center flex
                ${estatisticas.sentimento_predominante === 'positive' ? 'bg-green-100 text-green-700' : 
                  estatisticas.sentimento_predominante === 'negative' ? 'bg-red-100 text-red-700' : 
                  'bg-slate-100 text-slate-700'}`}>
                {estatisticas.sentimento_predominante}
              </span>
            </div>

            <div className="flex justify-between border-b pb-2">
              <span className="text-muted-foreground">Assimilação nota/sentimento:</span>
              <span className="font-medium">{estatisticas.assimiliacao_nota_sentimento.toFixed(2)}%</span>
            </div>

            <div className="flex justify-between pt-1">
              <span className="text-muted-foreground">Média global de confiança IA:</span>
              <span className="font-medium">{(estatisticas.media_confianca_global_ia * 100).toFixed(2)}%</span>
            </div>
          </div>
        </div>

        {/* Gráficos */}
        <div className="grid md:grid-cols-2 gap-6 mt-6">
          
          {/* Gráfico 1: Distribuição (%) */}
          <Card className="shadow-sm">
            <CardContent className="h-72 p-6">
              <div className="mb-4">
                <h4 className="font-semibold text-center text-sm text-muted-foreground uppercase tracking-wider">Distribuição de Sentimentos</h4>
              </div>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sentimentosData}>
                  <XAxis 
                    dataKey="name" 
                    tickFormatter={(v) => v === 'positive' ? 'Positivo' : v === 'negative' ? 'Negativo' : 'Neutro'} 
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#64748b', fontSize: 12 }}
                    dy={10}
                  />
                  <YAxis 
                    tickFormatter={(value) => `${value}%`} 
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#64748b', fontSize: 12 }}
                  />
                  <Tooltip 
                    cursor={{ fill: '#f1f5f9' }}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    formatter={(value: number) => [`${value.toFixed(1)}%`, 'Percentual']}
                  />
                  <Bar dataKey="percentual" radius={[4, 4, 0, 0]} barSize={50}>
                    {sentimentosData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Gráfico 2: Confiança média IA*/}
          <Card className="shadow-sm">
            <CardContent className="h-72 p-6">
              <div className="mb-4">
                <h4 className="font-semibold text-center text-sm text-muted-foreground uppercase tracking-wider">Confiança Média da IA</h4>
              </div>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sentimentosData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <XAxis 
                     dataKey="name" 
                     tickFormatter={(v) => v === 'positive' ? 'Positivo' : v === 'negative' ? 'Negativo' : 'Neutro'}
                     axisLine={false}
                     tickLine={false}
                     tick={{ fill: '#64748b', fontSize: 12 }}
                     dy={10}
                  />
                  <YAxis 
                    domain={[0, 1]} 
                    tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} 
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#64748b', fontSize: 12 }}
                  />
                  <Tooltip 
                    cursor={{ fill: '#f1f5f9' }}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    formatter={(value: number) => [`${(value * 100).toFixed(2)}%`, 'Confiança']}
                  />
                  <Bar dataKey="media_confianca" radius={[4, 4, 0, 0]} barSize={50}>
                    {sentimentosData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[entry.name]} fillOpacity={0.8} />
                    ))}
                  </Bar>
                  <ReferenceLine y={0.85} stroke="#f97316" strokeDasharray="3 3">
                    <Label value="Meta Qualidade (85%)" position="insideTopRight" fill="#f97316" fontSize={11} offset={10} />
                  </ReferenceLine>

                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
          
        </div>
      </div>
    )
  } else {
    return (
      <div className="p-6 text-center text-muted-foreground bg-muted/30 rounded-lg border border-dashed">
        Estatísticas de sentimentos indisponíveis no momento.
      </div>
    )
  }
}