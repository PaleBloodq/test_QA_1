import useIsLoading from "../../../hooks/useIsLoading";
import { GameType } from "../../../types/gameType";
import GamesSlider from "../../common/GamesSlider";

export default function Leaders({ data = [] }: { data: GameType[] }) {

    const isLoading = useIsLoading(data[0])

    return (
        <div className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center mb-4">
                <h1 className="text-header">Лидеры продаж</h1>
            </div>
            <GamesSlider type="game" data={data} isLoading={isLoading} />
        </div>
    )
}
