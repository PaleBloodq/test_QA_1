import { Price, Publication } from "../../../../types/publicationType"

type SelectPlatformType = {
    publications: Publication[],
    setSelectedPlatform: (arg: string) => void,
    selected: string,
    selectedPlatform: string,
}

export default function SelectPlatform({ publications, setSelectedPlatform, selected, selectedPlatform }: SelectPlatformType) {
    return (
        <div className="w-full gap-2 flex mb-[13px]">
            {publications.find((publication: Publication) => publication.id === selected)?.price.map((price: Price) => {
                return (
                    <button onClick={() => setSelectedPlatform(price.platform)} className={`w-full h-[33px] text-[14px] ${price.platform === selectedPlatform ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} key={price.platform}>
                        {price.platform}
                    </button>
                )
            })}
        </div>
    )
}
