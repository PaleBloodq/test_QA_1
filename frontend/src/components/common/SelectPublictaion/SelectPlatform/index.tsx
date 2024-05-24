import { useDispatch, useSelector } from "react-redux"
import { Publication } from "../../../../types/PublicationType"
import { selectedPlatformSelector } from "../../../../features/Game/publicationSelectors"
import { setSelectedPlatform } from "../../../../features/Game/publicationSlice"
import { useCallback, useEffect, useState } from "react"

type SelectPlatformType = {
    publications: Publication[],
}


export default function SelectPlatform({ publications }: SelectPlatformType) {
    const dispatch = useDispatch()
    const [samePlatforms, setSamePlatforms] = useState(false)

    const selectedPlatform = useSelector(selectedPlatformSelector)

    const haveIdenticalPlatforms = useCallback(
        (publications: Publication[]) => {
            if (publications.length === 0) {
                return true;
            }

            const firstPlatforms = publications[0].platforms;

            for (let i = 1; i < publications.length; i++) {
                const currentPlatforms = publications[i].platforms;
                if (firstPlatforms.length !== currentPlatforms.length) {
                    return false;
                }

                for (let j = 0; j < firstPlatforms.length; j++) {
                    if (firstPlatforms[j] !== currentPlatforms[j]) {
                        return false;
                    }
                }
            }
            return true;
        }, []
    );


    const platforms: string[] = []
    publications.forEach((item) => {
        item.platforms.forEach((item) => !platforms.includes(item) && platforms.push(item))
    }
    )

    useEffect(() => {
        dispatch(setSelectedPlatform(platforms[0]))
    }, [])

    useEffect(() => {
        if (publications) {
            setSamePlatforms(haveIdenticalPlatforms(publications))
        }
    }, [publications])


    return (
        !samePlatforms ?
            (<div className="w-full gap-2 flex mb-[13px]">
                {platforms?.map((platform, index) => {
                    return (
                        <button
                            onClick={() => dispatch(setSelectedPlatform(platform))}
                            className={`w-full h-[33px] text-[14px] ${platform === selectedPlatform ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} key={index}>
                            {platform}
                        </button>
                    )
                })}
            </div>) : <></>
    )
}
