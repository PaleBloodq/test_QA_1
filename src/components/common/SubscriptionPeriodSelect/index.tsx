type Props = {
    selectedPeriod: string,
    onPeriodChange: (period: string) => void,
}

const SubscriptionPeriodSelector = ({ selectedPeriod, onPeriodChange }: Props) => {
    const periods = ['1 месяц', '3 месяца', '12 месяцев'];

    return (
        <div className="flex w-full justify-between gap-2 mb-6">
            {periods.map(period => (
                <button
                    key={period}
                    onClick={() => onPeriodChange(period)}
                    className={"w-[110px] h-[33px] flex justify-center items-center bg-transparent text-sm rounded-lg " + (selectedPeriod === period ? "red-gradient text-white font-medium" : "border dark:border-[#FFFFFF1A] text-secondary-light dark:text-secondary-dark")}
                >
                    {period}
                </button>
            ))
            }
        </div >
    );
};

export default SubscriptionPeriodSelector;

// selectedPeriod === period