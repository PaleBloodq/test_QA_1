import useIsLoading from "../../../hooks/useIsLoading";
import { SectionType } from "../../../types/SectionType";
import GamesSlider from "../../common/GamesSlider";

export default function Leaders({ data }: { data: SectionType }) {

    const isLoading = useIsLoading(data?.objects?.length);

    return (
        <div className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center mb-4">
                <h1 className="text-header">Лидеры продаж</h1>
            </div>
            <GamesSlider type="GAME" data={data?.objects} isLoading={isLoading} />
        </div>
    )
}
