import gamepadIcon from "@icons/gamepad.svg";
import GamesSlider from "../../common/GamesSlider";
import { useGetSliderDonationsQuery } from "../../../services/sliderApi";

export default function Donation() {

    const { data = [], isLoading } = useGetSliderDonationsQuery({})

    console.log(data)

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
