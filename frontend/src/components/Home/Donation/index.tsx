import gamepadIcon from "@icons/gamepad.svg";
import GamesSlider from "../../common/GamesSlider";
import useIsLoading from "../../../hooks/useIsLoading";
import { SectionType } from "../../../types/SectionType";

export default function Donation({ data }: { data: SectionType }) {

    const isLoading = useIsLoading(data?.objects?.length);


    return (
        <div className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center mb-4">
                <img src={gamepadIcon} alt="donation" />
                <h1 className="text-header">Игровой донат</h1>
            </div>
            <GamesSlider type="DONATION" data={data?.objects} isLoading={isLoading} />
        </div>
    )
}
