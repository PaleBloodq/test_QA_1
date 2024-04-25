import { useDispatch } from "react-redux";
import { setDuration } from "../../../features/Subscription/subscriptionSlice";

const SubscriptionPeriodSelector = ({ selected }: { selected: number }) => {

    const periods = [1, 3, 12]
    const dispatch = useDispatch()

    const getPeriodLabel = (period: number) => {
        switch (period) {
            case 1:
                return 'месяц';
            case 3:
                return 'месяца';
            case 12:
                return 'месяцев';
            default:
                return '';
        }
    }

    return (
        <div className="flex w-full justify-between gap-2 mb-6">
            {periods.map(period => (
                <button
                    key={period}
                    onClick={() => dispatch(setDuration(period))}
                    className={"w-[110px] h-[33px] flex justify-center items-center bg-transparent text-sm rounded-lg " + (selected === period ? "red-gradient text-white font-medium" : "border dark:border-[#FFFFFF1A] text-secondary-light dark:text-secondary-dark")}
                >
                    {period} {getPeriodLabel(period)}
                </button>
            ))}
        </div >
    );
};

export default SubscriptionPeriodSelector;
