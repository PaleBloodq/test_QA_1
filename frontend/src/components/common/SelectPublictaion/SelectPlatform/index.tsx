import { useDispatch, useSelector } from "react-redux"
import { Publication } from "../../../../types/PublicationType"
import { selectedPlatformSelector, selectedPublicationSelector } from "../../../../features/Game/publicationSelectors"
import { setSelectedPlatform } from "../../../../features/Game/publicationSlice"
import { useEffect } from "react"

type SelectPlatformType = {
    publications: Publication[],
}


export default function SelectPlatform({ publications }: SelectPlatformType) {
    const dispatch = useDispatch()

    const selectedPlatform = useSelector(selectedPlatformSelector)


    const platforms: string[] = []
    publications.forEach((item) => {
        item.platforms.forEach((item) => !platforms.includes(item) && platforms.push(item))
    }
    )

    useEffect(() => {
        dispatch(setSelectedPlatform(platforms[0]))
    }, [])


    return (
        <div className="w-full gap-2 flex mb-[13px]">
            {platforms?.map((platform, index) => {
                return (
                    <button
                        onClick={() => dispatch(setSelectedPlatform(platform))}
                        className={`w-full h-[33px] text-[14px] ${platform === selectedPlatform ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} key={index}>
                        {platform}
                    </button>
                )
            })}
        </div>
    )
}
