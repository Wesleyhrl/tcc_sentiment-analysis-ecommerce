import Link from 'next/link';
import Image from 'next/image';
import { ExternalLink, Menu } from 'lucide-react';
import {
    Sheet,
    SheetContent,
    SheetTrigger,
    SheetTitle,
    SheetDescription,
} from "@/components/ui/sheet";

export default function Header() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL_DOCS || 'http://127.0.0.1:8000/docs';

    return (
        <header className="sticky top-0 z-50 bg-primary-blue shadow-lg">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">

                {/*LOGO*/}
                <Link href="/" className="flex items-center gap-3 hover:opacity-90 transition-opacity group">
                    <div className="relative">
                        <Image
                            src="/icon.svg"
                            alt="Logo Review Sentimentum"
                            width={40}
                            height={40}
                            priority
                            className="scale-120 group-hover:scale-130 transition-transform duration-200"
                        />
                    </div>
                    <h1 className="text-white text-lg md:text-2xl font-bold tracking-wide">
                        Review Sentimentum
                    </h1>
                </Link>

                {/*NAVEGAÇÃO DESKTOP*/}
                <nav className="hidden md:flex items-center gap-6">
                    <Link href="/" className="text-gray-100 hover:text-white font-medium transition-colors text-sm">
                        Início
                    </Link>

                    <Link href="/sobre" className="text-gray-100 hover:text-white font-medium transition-colors text-sm">
                        Sobre o Projeto
                    </Link>

                    <div className="h-4 w-px bg-blue-400/50"></div>

                    <Link
                        href={apiUrl}
                        target="_blank"
                        className="text-blue-200 hover:text-white font-medium transition-colors text-xs flex items-center gap-1"
                        title="Documentação para Desenvolvedores (Swagger UI)"
                    >
                        <span>API Docs</span>
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><ExternalLink /></svg>
                    </Link>

                    <Link
                        href="https://github.com/Wesleyhrl/tcc_sentiment-analysis-ecommerce"
                        target="_blank"
                        className="hover:opacity-80 transition-opacity"
                        aria-label="Ver código no GitHub"
                    >
                        <Image
                            src="/github-mark-white.svg"
                            alt="GitHub"
                            width={24}
                            height={24}
                            priority
                        />
                    </Link>
                </nav>

                {/*NAVEGAÇÃO MOBILE*/}
                <div className="md:hidden">
                    <Sheet >
                        <SheetTrigger asChild>
                            <button 
                                className="text-white p-2 hover:bg-white/10 rounded-md transition-colors"
                                aria-label="Abrir menu"
                            >
                                <Menu className="w-6 h-6" />
                            </button>
                        </SheetTrigger>
                        
                        <SheetContent side="right" className="p-4 bg-primary-blue border-l-blue-400/30 text-white w-[300px]">
                            <SheetTitle className="text-white font-bold text-lg mb-6 border-b border-blue-400/30 pb-4">
                                Menu
                            </SheetTitle>

                            <SheetDescription className="sr-only">
                                Navegação principal mobile
                            </SheetDescription>

                            <nav className="flex flex-col gap-6">
                                <Link href="/" className="text-gray-100 hover:text-white text-lg font-medium transition-colors">
                                    Início
                                </Link>

                                <Link href="/sobre" className="text-gray-100 hover:text-white text-lg font-medium transition-colors">
                                    Sobre o Projeto
                                </Link>

                                <div className="h-px w-full bg-blue-400/30 my-2"></div>

                                <Link
                                    href={apiUrl}
                                    target="_blank"
                                    className="text-blue-200 hover:text-white font-medium transition-colors flex items-center gap-2"
                                >
                                    <span>API Docs</span>
                                    <ExternalLink className="w-4 h-4" />
                                </Link>

                                <Link
                                    href="https://github.com/Wesleyhrl/tcc_sentiment-analysis-ecommerce"
                                    target="_blank"
                                    className="flex items-center gap-3 hover:opacity-80 transition-opacity mt-2"
                                >
                                    <Image
                                        src="/github-mark-white.svg"
                                        alt="GitHub"
                                        width={24}
                                        height={24}
                                    />
                                    <span className="text-sm font-medium">Ver no GitHub</span>
                                </Link>
                            </nav>
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </header>
    );
}