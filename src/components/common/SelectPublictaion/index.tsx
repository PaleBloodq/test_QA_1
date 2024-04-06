import { useEffect } from "react"
import { PriceType, Publication } from "../../../types/publicationType"
import SelectPlatform from "./SelectPlatform"
import { useDispatch, useSelector } from "react-redux"
import { selectedPlatformSelector, selectedPublicationSelector } from "../../../features/Game/publicationSelectors"
import { setSelectedPlatform, setSelectedPublication } from "../../../features/Game/publicationSlice"

type SelectPublicationType = {
    publications: Publication[],
}

export default function SelectPublication({ publications }: SelectPublicationType) {
    const dispatch = useDispatch()

    const selectedPublication = useSelector(selectedPublicationSelector)

    const selectedPlatform = useSelector(selectedPlatformSelector)
    useEffect(() => {
        dispatch(setSelectedPlatform(publications[0]?.price[0]?.platform))
    }, [])



    return (
        <>
            <h2 className="text-title-xl mb-[18px]">Издания</h2>
            <SelectPlatform publications={publications} />
            <div className="w-full gap-3 flex justify-between">
                {publications.map((publication) => {
                    return (
                        <button
                            onClick={() => dispatch(setSelectedPublication(publication.id))}
                            key={publication.id}
                            className={`w-full h-20 flex flex-col justify-center items-center ${publication.id == selectedPublication ? 'custom-border__red' : 'custom-border'}`}
                            disabled={publication?.price?.find((price: PriceType) => price.platform === selectedPlatform)?.price === undefined}
                        >
                            <h1 className="text-subtitle">{publication.title}</h1>
                            <h2 className="price-small">
                                {
                                    publication?.price?.find((price: PriceType) => price.platform === selectedPlatform)?.price !== undefined ?
                                        (publication?.price?.find((price: PriceType) => price.platform === selectedPlatform)?.price + "₽") :
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
