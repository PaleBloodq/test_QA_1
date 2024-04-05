import lightningIcon from "@icons/lightning.svg";
import GamesSlider from "../../common/GamesSlider";
import useIsLoading from "../../../hooks/useIsLoading";
import { gameType } from "../../../types/gameType";

export default function NewGames({ data }: { data: gameType[] }) {

    const isLoading = useIsLoading(data && data.length | 0)


    return (
        <div className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center mb-4">
                <img src={lightningIcon} alt="new" />
                <h1 className="text-header">Новинки</h1>
            </div>
            <GamesSlider type="game" data={data} isLoading={isLoading} />
        </div>
    )
}
