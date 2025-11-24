import { Spinner } from "@/components/ui/spinner"

interface LoadingComponentProps {
    titulo?: string;
}

export default function LoadingComponent({ titulo }: LoadingComponentProps) {

    return (
        <div className="flex flex-col items-center space-y-2 p-3">
            <Spinner className="size-10 text-gray-600" />
            {titulo &&<h2 className="font-medium italic text-gray-400">{titulo}</h2>}
        </div>
    )

}