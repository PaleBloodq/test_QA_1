import lightningIcon from "@icons/lightning.svg";
import GamesSlider from "../../common/GamesSlider";
import useIsLoading from "../../../hooks/useIsLoading";
import { SectionType } from "../../../types/SectionType";

export default function NewGames({ data }: { data: SectionType }) {

    const isLoading = useIsLoading(data?.objects.length);


    return (
        <div className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center mb-4">
                <img src={lightningIcon} alt="new" />
                <h1 className="text-header">Новинки</h1>
            </div>
            <GamesSlider type="GAME" data={data?.objects} isLoading={isLoading} />
        </div>
    )
}
