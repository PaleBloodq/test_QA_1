import lightningIcon from "@icons/lightning.svg";
import GamesSlider from "../../common/GamesSlider";
import useIsLoading from "../../../hooks/useIsLoading";
import { SectionType } from "../../../types/SectionType";

export default function NewGames({ data }: { data: SectionType }) {

    const isLoading = useIsLoading(data?.products.length);


    return (
        <div className="w-screen relative -ml-[15px]">
            <div className="max-w-[560px] mx-auto mt-7 pt-6 pb-3 px-0 custom-border flex flex-col">
                <div className="flex gap-3 items-center mb-4">
                    <img className="ml-5" src={lightningIcon} alt="new" />
                    <h1 className="text-header">Новинки</h1>
                </div>
                <div className="ml-2">
                    <GamesSlider type="GAME" data={data?.products} isLoading={isLoading} />
                </div>
            </div>
        </div>
    );
}
