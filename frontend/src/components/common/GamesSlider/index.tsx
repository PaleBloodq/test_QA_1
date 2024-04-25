import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import './newGamesSlider.css';
import { Pagination } from 'swiper/modules';
import React from 'react';
import { donationType } from '../../../types/donationType';
import GameCard from '../GameCard';
import { GameType } from '../../../types/gameType';
import DonationCard from '../DonationCard';

type GamesData = GameType[];
type DonationsData = donationType[];

type GamesSliderProps = {
    data: GamesData | DonationsData;
    isLoading: boolean;
    type?: "game" | "donation";
}

const GamesSlider = React.memo(({ data, isLoading, type }: GamesSliderProps) => {
    return (
        <>
            {!isLoading &&
                <Swiper
                    slidesPerView={"auto"}
                    spaceBetween={15}
                    pagination={false}
                    modules={[Pagination]}
                    className="newGamesSlider"
                >
                    {data.map((item, index) => {
                        return <SwiperSlide key={index}>
                            {type === "game" ? (
                                <GameCard game={item as GameType} />
                            ) : type === "donation" ? (
                                <DonationCard donation={item as donationType} />
                            ) : null}
                        </SwiperSlide>
                    })}
                </Swiper>
            }
        </>
    );
});

export default GamesSlider;