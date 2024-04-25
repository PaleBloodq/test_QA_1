import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import './newGamesSlider.css';
import { Pagination } from 'swiper/modules';
import React from 'react';
import GameCard from '../GameCard';
import { ProductType } from '../../../types/ProductType';
import DonationCard from '../DonationCard';
import SubscriptionCard from '../SubscriptionCard';


type GamesSliderProps = {
    data: ProductType[];
    isLoading: boolean;
    type?: "GAME" | "DONATION" | "SUBSCRIPTION";
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
                            {/* {type === "GAME" ? (
                                <GameCard game={item} />
                            ) : type === "DONATION" ? (
                                <DonationCard donation={item} />
                            ) : null} */}
                            {type === "GAME" && <GameCard game={item} />}
                            {type === "DONATION" && <DonationCard donation={item} />}
                            {type === "SUBSCRIPTION" && <SubscriptionCard subscription={item} />}
                        </SwiperSlide>
                    })}
                </Swiper>
            }
        </>
    );
});

export default GamesSlider;