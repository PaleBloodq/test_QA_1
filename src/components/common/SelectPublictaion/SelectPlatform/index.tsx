import { useSelector } from "react-redux"
import { Price, Publication } from "../../../../types/publicationType"
import { selectedPublicationSelector } from "../../../../features/Game/publicationSelectors"

type SelectPlatformType = {
    publications: Publication[],
    setSelectedPlatform: (arg: string) => void,
    selectedPlatform: string,
}


export default function SelectPlatform({ publications, setSelectedPlatform, selectedPlatform }: SelectPlatformType) {
    const selectedPublication = useSelector(selectedPublicationSelector)
    return (
        <div className="w-full gap-2 flex mb-[13px]">
            {publications.find((publication: Publication) => publication.id === selectedPublication)?.price.map((price: Price) => {
                return (
                    <button onClick={() => setSelectedPlatform(price.platform)} className={`w-full h-[33px] text-[14px] ${price.platform === selectedPlatform ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} key={price.platform}>
                        {price.platform}
                    </button>
                )
            })}
        </div>
    )
}
