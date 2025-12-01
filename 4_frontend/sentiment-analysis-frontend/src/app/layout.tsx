import "./globals.css";
import Header from './../components/header/index';
import type { Metadata } from 'next';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL 
  ? `https://${process.env.NEXT_PUBLIC_SITE_URL}` 
  : 'http://localhost:3000/';

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: "Review Sentimentum | Análise de Sentimentos com IA",
    template: "%s | Review Sentimentum",
  },
  description: "Plataforma para análise de sentimentos em avaliações de e-commerce utilizando Processamento de Linguagem Natural (NLP) e Inteligência Artificial.",
  keywords: ["Análise de Sentimentos", "NLP", "IA", "TCC", "E-commerce", "Reviews", "React","Next.js","TailwindCSS"],
  authors: [{ name: "Wesley Henrique", url: "https://github.com/Wesleyhrl" }],
  creator: "Wesley Henrique",
  icons: {
    icon: "/icon.svg",
  },
  openGraph: {
    title: "Review Sentimentum - Análise de Sentimentos",
    description: "Descubra a análise de sentimentos em avaliações de e-commerce usando Inteligência Artificial.",
    siteName: "Review Sentimentum",
    locale: "pt_BR",
    type: "website",
  },
  robots: {
    index: true,
    follow: true,
  },
};




export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased flex flex-col min-h-screen">
        <Header />
        <main className="flex-1">
          {children}
        </main>
      </body>
    </html>
  );
}
