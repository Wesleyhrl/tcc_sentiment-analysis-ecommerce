"use client"


import {
    ArrowLeftIcon,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"

export function CategoryMenuTeste() {

    return (
        <ScrollArea type="auto" className="w-full  pb-4 whitespace-nowrap">
            <ButtonGroup className="w-full flex justify-center">
                <ButtonGroup>
                    <Button variant="outline" size="icon" aria-label="Go Back">
                        <ArrowLeftIcon /> {/*voltar*/}
                    </Button>
                </ButtonGroup>
                <ButtonGroup>
                    <Button variant="outline">Coolers</Button>
                    <Button variant="outline">Disco</Button>
                    <Button variant="outline">Disco</Button>
                    <Button variant="outline">Disco</Button>
                    <Button variant="outline">Disco</Button>
                    <Button variant="outline">Disco</Button>
                </ButtonGroup>
            </ButtonGroup>
            <ScrollBar orientation="horizontal" />
        </ScrollArea>
    )
}