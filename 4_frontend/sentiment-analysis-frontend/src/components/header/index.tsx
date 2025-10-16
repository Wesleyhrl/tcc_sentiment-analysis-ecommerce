import Link from 'next/link'

export default function Header() {
    return (
        <header className="bg-primary-blue p-4 flex justify-center">
            <h1 className="text-text-secondary text-2xl  font-bold" ><Link href="/">Review Sentimentum</Link></h1>
        </header>
    );
}