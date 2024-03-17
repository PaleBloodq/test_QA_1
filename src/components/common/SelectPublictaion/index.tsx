import { useState } from "react"
import { Price, Publication } from "../../../types/publicationType"
import SelectPlatform from "./SelectPlatform"

type SelectPublicationType = {
    publications: Publication[],
    selected: string,
    setSelected: (arg: string) => void
}

export default function SelectPublication({ publications, selected, setSelected }: SelectPublicationType) {

    const [selectedPlatform, setSelectedPlatform] = useState(publications[0]?.price[0]?.platform || "null")

    console.log(selected)


    return (
        <>
            <h2 className="text-title text-[18px] mb-[18px]">Издания</h2>
            <SelectPlatform publications={publications} setSelectedPlatform={setSelectedPlatform} selected={selected} selectedPlatform={selectedPlatform} />
            <div className="w-full gap-3 flex justify-between">
                {publications.map((publication) => {
                    return (
                        <button
                            onClick={() => setSelected(publication.id)}
                            key={publication.id}
                            className={`w-full h-20 flex flex-col justify-center items-center ${publication.id == selected ? 'custom-border__red' : 'custom-border'}`}
                            disabled={publication?.price?.find((price: Price) => price.platform === selectedPlatform)?.price === undefined}
                        >
                            <h1 className="text-subtitle">{publication.title}</h1>
                            <h2 className="price-small">
                                {
                                    publication?.price?.find((price: Price) => price.platform === selectedPlatform)?.price !== undefined ?
                                        (publication?.price?.find((price: Price) => price.platform === selectedPlatform)?.price + "₽") :
                                        'Нет в наличии'
                                }
                            </h2>
                        </button>
                    )

                })}
            </div >
        </>
    )
}
