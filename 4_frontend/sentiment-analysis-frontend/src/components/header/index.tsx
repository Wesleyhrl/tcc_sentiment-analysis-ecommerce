import Link from 'next/link';
import Image from 'next/image';
import { ExternalLink } from 'lucide-react';

export default function Header() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL_DOCS || 'http://127.0.0.1:8000/docs';

    return (
        <header className="sticky top-0 z-50 bg-primary-blue shadow-lg">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">

                <Link href="/" className="flex items-center gap-3 hover:opacity-90 transition-opacity group">
                    <div className="relative">
                        <Image
                            src="/icon.svg"
                            alt="Logo Review Sentimentum"
                            width={40} 
                            height={40}
                            priority
                            className="group-hover:scale-110 transition-transform duration-200"
                        />
                    </div>
                    <h1 className="text-white text-lg md:text-2xl font-bold tracking-wide">
                        Review Sentimentum
                    </h1>
                </Link>

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
            </div>
        </header>
    );
}