import { PublicationType } from "../../../types/PublicationType"
import SelectPlatform from "./SelectPlatform"
import { useDispatch, useSelector } from "react-redux"
import { selectedPlatformSelector, selectedPublicationSelector } from "../../../features/Game/publicationSelectors"
import { setSelectedPublication } from "../../../features/Game/publicationSlice"

type SelectPublicationType = {
    publications: PublicationType[],
}

export default function SelectPublication({ publications }: SelectPublicationType) {
    const dispatch = useDispatch()

    const selectedPublication = useSelector(selectedPublicationSelector)
    const selectedPlatform = useSelector(selectedPlatformSelector)

    return (
        <>
            <h2 className="text-title-xl mb-[18px]">Издания</h2>
            <SelectPlatform publications={publications} />
            <div className="w-full gap-3 flex justify-start flex-wrap">
                {publications
                    .filter((publication) => selectedPlatform === undefined || publication.platforms.includes(selectedPlatform))
                    .map((publication) => (
                        <button
                            key={publication.id}
                            onClick={() => dispatch(setSelectedPublication(publication.id))}
                            className={`w-full max-w-[160px] h-20 flex flex-col justify-center items-center ${publication.id === selectedPublication ? 'custom-border__red' : 'custom-border'
                                }`}
                        >
                            <h1 className="text-subtitle text-center">{publication.title}</h1>
                            <h2 className="price-small">
                                {publication.final_price}₽
                            </h2>
                        </button>
                    ))}
            </div>
        </>
    )
}