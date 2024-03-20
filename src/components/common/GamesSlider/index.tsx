import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import './newGamesSlider.css';
import { Pagination } from 'swiper/modules';
import Tag from '../Tag';
import { Link } from 'react-router-dom';
import { getDiscount } from '../../../hooks/getDiscount';
import React from 'react';
import { gameType } from '../../../types/gameType';
import { donationType } from '../../../types/donationType';

type GamesData = gameType[];
type DonationsData = donationType[];

type GamesSliderProps = {
    data: GamesData | DonationsData;
    isLoading: boolean;
    type?: "game" | "donation";
}

const GameCard = React.memo(({ game }: { game: gameType }) => {
    const { title, photoUrls, publications } = game;
    const { price, discount } = publications[0];

    return (
        <Link to={'/game/' + game.id} className='w-full h-full flex flex-col items-start justify-between'>
            <img className='rounded-xl max-h-[200px] mb-[18px]' src={photoUrls[0]} alt="game image" />
            <h1 className='text-title text-start'>{title}</h1>
            {publications && <h2 className='text-subtitle'>{publications[0].title}</h2>}
            <div className='flex gap-2'>
                <h3 className='price-small'>
                    {discount.percent && discount.percent > 0
                        ? getDiscount(price[0].price, discount.percent)
                        : price[0].price} ₽
                </h3>
                {discount.percent !== 0 &&
                    <Tag type="discount">-{discount.percent}%</Tag>}
            </div>
        </Link>
    );
});

const DonationCard = React.memo(({ donation }: { donation: donationType }) => {
    return (
        <Link to={'/donation/' + donation.id} className='w-full h-[240px] flex flex-col items-start justify-between'>
            <img className='h-full rounded-xl mb-[18px]' src={donation.previewImg} alt="donation image" />
        </Link>
    );
});

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
                    {data.map((item, index) => (
                        <SwiperSlide key={index}>
                            {type === "game" ? (
                                <GameCard game={item as gameType} />
                            ) : type === "donation" ? (
                                <DonationCard donation={item as donationType} />
                            ) : null}
                        </SwiperSlide>
                    ))}
                </Swiper>
            }
        </>
    );
});

export default GamesSlider;