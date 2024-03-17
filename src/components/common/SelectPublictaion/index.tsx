import { useState } from "react"
import { Price, Publication } from "../../../types/publicationType"
import SelectPlatform from "./SelectPlatform"
import { useDispatch, useSelector } from "react-redux"
import { selectedPublicationSelector } from "../../../features/Game/publicationSelectors"
import { setSelectedPublication } from "../../../features/Game/publicationSlice"

type SelectPublicationType = {
    publications: Publication[],
}

export default function SelectPublication({ publications }: SelectPublicationType) {
    const dispatch = useDispatch()

    const selectedPublication = useSelector(selectedPublicationSelector)

    const [selectedPlatform, setSelectedPlatform] = useState(publications[0]?.price[0]?.platform || "null")



    return (
        <>
            <h2 className="text-title text-[18px] mb-[18px]">Издания</h2>
            <SelectPlatform publications={publications} setSelectedPlatform={setSelectedPlatform} selectedPublication={selectedPublication} selectedPlatform={selectedPlatform} />
            <div className="w-full gap-3 flex justify-between">
                {publications.map((publication) => {
                    return (
                        <button
                            onClick={() => dispatch(setSelectedPublication(publication.id))}
                            key={publication.id}
                            className={`w-full h-20 flex flex-col justify-center items-center ${publication.id == selectedPublication ? 'custom-border__red' : 'custom-border'}`}
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
