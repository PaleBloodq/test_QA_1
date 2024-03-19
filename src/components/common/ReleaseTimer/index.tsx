import { useState, useEffect } from "react";

export default function ReleaseTimer({ releaseDate }: { releaseDate: string }) {
    const [difference, setDifference] = useState([0, 0, 0, 0]);

    function getTimeDifference(targetDateISO: string) {
        const targetDate = new Date(targetDateISO);
        const currentDate = new Date();

        let timeDiff = targetDate.getTime() - currentDate.getTime();

        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
        timeDiff -= days * (1000 * 60 * 60 * 24);

        const hours = Math.floor(timeDiff / (1000 * 60 * 60));
        timeDiff -= hours * (1000 * 60 * 60);

        const minutes = Math.floor(timeDiff / (1000 * 60));
        timeDiff -= minutes * (1000 * 60);

        const seconds = Math.floor(timeDiff / 1000);

        setDifference([days, hours, minutes, seconds]);
    }

    useEffect(() => {
        const intervalId = setInterval(() => {
            getTimeDifference(releaseDate);
        }, 1000);

        // Очистка интервала при размонтировании компонента
        return () => clearInterval(intervalId);
    }, [releaseDate]); // Зависимости useEffect

    return (
        <div className="flex flex-col gap-5 mt-[32px] w-full">
            <h1 className="text-title text-[18px]">До релиза:</h1>
            <div className="custom-border min-h-20 justify-center flex gap-10 py-2">
                <div className="flex flex-col items-center">
                    <h1 className={difference[0] ? "price-big" : "price-big text-secondary-light dark:text-secondary-dark"}>{difference[0]}</h1>
                    <p className="text-subtitle">Дней</p>
                </div>
                <div className="flex flex-col items-center">
                    <h1 className={difference[1] ? "price-big" : "price-big text-secondary-light dark:text-secondary-dark"}>{difference[1]}</h1>
                    <p className="text-subtitle">Часов</p>
                </div>
                <div className="flex flex-col items-center">
                    <h1 className={difference[2] ? "price-big" : "price-big text-secondary-light dark:text-secondary-dark"}>{difference[2]}</h1>
                    <p className="text-subtitle">Минут</p>
                </div>
                <div className="flex flex-col items-center">
                    <h1 className={difference[3] ? "price-big" : "price-big text-secondary-light dark:text-secondary-dark"}>{difference[3]}</h1>
                    <p className="text-subtitle">Секунд</p>
                </div>
            </div>
        </div>
    );
}
