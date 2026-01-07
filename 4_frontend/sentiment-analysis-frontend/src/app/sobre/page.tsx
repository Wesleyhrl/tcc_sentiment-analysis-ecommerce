import Link from 'next/link';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
    Bot,
    BrainCircuit,
    Zap,
    CheckCircle2,
    Code2,
    GraduationCap, // Novo
    User,          // Novo
    FileText,      // Novo
    Linkedin,      // Novo (ou use o Github existente se o lucide não tiver o brand icon, mas geralmente tem)
    Github
} from "lucide-react";
import Image from 'next/image';

export default function AboutPage() {
    return (
        <div className="min-h-screen bg-gray-50/50 pb-12">

            {/*Sobre*/}
            <div className="bg-white">
                <div className="container mx-auto px-4 py-16 text-center">
                    <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6 tracking-tight">
                        Sobre o Review Sentimentum
                    </h1>
                    <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
                        Uma ferramenta inteligente que utiliza Processamento de Linguagem Natural (NLP) para auxiliar consumidores,
                        transformando milhares de comentários em melhores decisões de compra de produtos de informática.
                    </p>
                </div>
                <Separator />
            </div>

            <div className="container mx-auto px-4 py-12 space-y-20">

                {/*O Desafio*/}
                <section className="grid md:grid-cols-2 gap-12 items-center">
                    <div className="space-y-6">
                        <div className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-sm font-medium text-blue-800">
                            Contexto
                        </div>
                        <h2 className="text-3xl font-bold tracking-tight text-slate-900">O Desafio</h2>
                        <div className="text-lg text-slate-600 space-y-4">
                            <p>
                                Sites de e-commerce como a Kabum possuem milhares de avaliações.
                                Ler todas elas para entender se uma placa de vídeo esquenta muito ou
                                se um monitor tem <em>dead pixels</em> é uma tarefa exaustiva.
                            </p>
                            <p>
                                Muitas vezes, a nota geral (estrelas) esconde detalhes técnicos cruciais.
                                O consumidor precisa saber se o produto &quot;dá gargalo&quot; ou se tem &quot;coil whine&quot;,
                                e não apenas se ele é &quot;bom&quot;.
                            </p>
                        </div>
                    </div>

                    {/* Card de Solução */}
                    <Card className="border-l-4 border-l-green-500 shadow-md">
                        <CardHeader>
                            <CardTitle className="text-green-600 flex items-center gap-2">
                                <Zap className="h-5 w-5" />
                                Nossa Solução
                            </CardTitle>
                            <CardDescription>
                                Automação e Inteligência Artificial aplicadas
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <p className="text-slate-700">
                                O <strong>Review Sentimentum</strong> lê cada comentário, identifica o sentimento
                                (Positivo, Negativo ou Neutro) e gera insights estatísticos.
                            </p>
                            <ul className="space-y-3 mt-4">
                                <li className="flex items-center gap-3 text-slate-700">
                                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                                    <span>Economia de tempo na pesquisa</span>
                                </li>
                                <li className="flex items-center gap-3 text-slate-700">
                                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                                    <span>Análise imparcial via IA (RoBERTa)</span>
                                </li>
                                <li className="flex items-center gap-3 text-slate-700">
                                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                                    <span>Foco no nicho de Informática</span>
                                </li>
                            </ul>
                        </CardContent>
                    </Card>
                </section>

                {/* Seção: Como Funciona (Tech Stack) */}
                <section>
                    <div className="text-center mb-10">
                        <h2 className="text-3xl font-bold text-slate-900 mb-4">Como Funciona (Tech Stack)</h2>
                        <p className="text-slate-600">A arquitetura por trás do projeto</p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6">
                        {/* Card 1: Coleta */}
                        <Card className="hover:shadow-lg transition-all duration-300 border-t-4 border-t-blue-500">
                            <CardHeader>
                                <Bot className="h-10 w-10 text-blue-500 mb-2" />
                                <CardTitle>Coleta de Dados</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-600">
                                    Utilizamos <strong>Python e Selenium</strong> para navegar nas páginas de produtos
                                    e extrair comentários reais de forma ética e estruturada.
                                </p>
                            </CardContent>
                        </Card>

                        {/* Card 2: IA */}
                        <Card className="hover:shadow-lg transition-all duration-300 border-t-4 border-t-purple-500">
                            <CardHeader>
                                <BrainCircuit className="h-10 w-10 text-purple-500 mb-2" />
                                <CardTitle>Análise de Sentimento</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-600">
                                    Os textos são processados por um modelo <strong>RoBERTa</strong> (Transformer)
                                    fine-tuned, capaz de entender contextos do PT-BR.
                                </p>
                            </CardContent>
                        </Card>

                        {/* Card 3: Web App */}
                        <Card className="hover:shadow-lg transition-all duration-300 border-t-4 border-t-amber-500">
                            <CardHeader>
                                <Code2 className="h-10 w-10 text-amber-500 mb-2" />
                                <CardTitle>Aplicação Web</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-slate-600">
                                    Arquitetura moderna (FARM Stack): Backend robusto em <strong>FastAPI</strong> integrado ao <strong>MongoDB</strong>,
                                    servindo um frontend moderno e reativo em <strong>Next.js</strong>.
                                </p>
                            </CardContent>
                        </Card>
                    </div>
                </section>

                {/* AcadêmicO e Autor */}
                <section>
                    <div className="text-center mb-10">
                        <h2 className="text-3xl font-bold text-slate-900 mb-4">Sobre o projeto</h2>
                    </div>
                    <Card className="bg-white border-t-4 border-t-slate-800 shadow-lg overflow-hidden">
                        <div className="grid md:grid-cols-2 gap-0">

                            {/* Lado Esquerdo: Contexto Acadêmico */}
                            <div className="p-8 md:p-12  flex flex-col justify-center">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="p-3 bg-blue-100 rounded-lg">
                                        <GraduationCap className="h-6 w-6 text-blue-700" />
                                    </div>
                                    <h2 className="text-2xl font-bold text-slate-900">Contexto Acadêmico</h2>
                                </div>

                                <p className="text-slate-600 mb-6 leading-relaxed">
                                    Projeto desenvolvido como Trabalho de Conclusão de Curso (TCC)
                                    para o Bacharelado em <strong>Sistemas de Informação</strong>.
                                </p>

                                <ul className="space-y-3 text-sm text-slate-500">
                                    <li className="flex items-center gap-2">
                                        <span className="font-semibold text-slate-700">Instituição:</span>
                                        Pontifícia Universidade Católica de Minas Gerais (PUC Minas)
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <span className="font-semibold text-slate-700">Ano/Semestre:</span>
                                        2025 / 2º Semestre
                                    </li>
                                </ul>
                            </div>

                            {/* Lado Direito: Sobre o Autor & Links */}
                            <div className="p-8 md:p-12 flex flex-col justify-center border-l border-slate-100">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="p-3 bg-slate-100 rounded-lg">
                                        <User className="h-6 w-6 text-slate-700" />
                                    </div>
                                    <h2 className="text-2xl font-bold text-slate-900">O Autor</h2>
                                </div>

                                <p className="text-slate-600 mb-8 leading-relaxed">
                                    Desenvolvido por <strong>Wesley Henrique</strong>.
                                    O objetivo é demonstrar a aplicação prática de técnicas de Inteligência Artificial
                                    modernas em problemas reais do cotidiano do consumidor brasileiro.
                                </p>

                                <div className="flex flex-wrap gap-4">
                                    {/* Botão GitHub */}
                                    <Button asChild variant="outline" className="gap-2 border-slate-300 hover:bg-slate-100 text-slate-700">
                                        <Link href="https://github.com/Wesleyhrl/tcc_sentiment-analysis-ecommerce" target="_blank">
                                            <Image
                                                src="/github-mark.svg"
                                                alt="GitHub"
                                                width={20}
                                                height={20}
                                                priority
                                            />
                                            Repositório
                                        </Link>
                                    </Button>

                                    {/*Botão LinkedIn*/}
                                    <Button asChild className="gap-2 bg-[#0077b5] hover:bg-[#005582] text-white">
                                        <Link href="https://www.linkedin.com/in/wesleyhrl" target="_blank">
                                            <Image
                                                src="/linkedin-icon-white.svg"
                                                alt="GitHub"
                                                width={20}
                                                height={20}
                                                priority
                                            />
                                            LinkedIn
                                        </Link>
                                    </Button>

                                    {/* Botão Documentação/Artigo*/}
                                    <Button asChild variant="outline" className="gap-2 border-slate-300 hover:bg-slate-100 text-slate-700">
                                        <Link href="/tcc.pdf" target="_blank">
                                            <FileText />
                                            Ler Artigo
                                        </Link>
                                    </Button>

                                </div>
                            </div>
                        </div>
                    </Card>
                </section>
            </div>
        </div>
    );
}