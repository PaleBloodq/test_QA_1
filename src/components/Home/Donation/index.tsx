import gamepadIcon from "@icons/gamepad.svg";
import GamesSlider from "../../common/GamesSlider";
import useIsLoading from "../../../hooks/useIsLoading";

export default function Donation({ data = [] }) {

    const isLoading = useIsLoading(data[0])

    return (
        <div className="mt-7 pt-6 pb-3 px-4 custom-border flex flex-col">
            <div className="flex gap-3 items-center mb-4">
                <img src={gamepadIcon} alt="donation" />
                <h1 className="text-header">Игровой донат</h1>
            </div>
            <GamesSlider type="donation" data={data} isLoading={isLoading} />
        </div>
    )
}
