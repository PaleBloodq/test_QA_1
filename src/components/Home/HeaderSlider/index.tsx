import { useEffect, useRef } from 'react';
import { useGetSliderGamesQuery } from "../../../services/sliderApi"
import { differenceInMonths, parseISO } from 'date-fns';
import { Swiper, SwiperSlide } from 'swiper/react';
import { getDiscount } from '../../../hooks/getDiscount';

import 'swiper/css';
import 'swiper/css/pagination';

import './headerSlider.css';
import Tag from '../../common/Tag';
import { gameType } from '../../../types/gameType';
import { Link } from 'react-router-dom';

export default function HeaderSlider() {
    const { data = [], isLoading } = useGetSliderGamesQuery({});
    const swiperRef = useRef(null);

    useEffect(() => {
        if (swiperRef.current) {
            const swiper = swiperRef.current.swiper;
            swiper.slides[swiper.activeIndex].classList.add('active');
            swiper.on('slideChange', () => {
                swiper.slides.forEach((slide: Element) => slide.classList.remove('active'));
                swiper.slides[swiper.activeIndex].classList.add('active');
            });
        }
    }, []);



    return (
        <div className="h-[355px] w-full">
            {!isLoading && (
                <Swiper
                    slidesPerView={"auto"}
                    centeredSlides={true}
                    spaceBetween={13}
                    pagination={false}
                    className="headerSwiper"
                    ref={swiperRef}
                >
                    {data.map((game: gameType, index: number) => {
                        const releaseDate = parseISO(game.releaseDate);
                        const isNew = differenceInMonths(new Date(), releaseDate) < 2;

                        return (
                            <SwiperSlide key={`header-${index}`}>
                                <Link className="flex w-full h-full relative" to={"/game/" + game.id}>
                                    <img className="rounded-xl" src={game.previewImg} alt="" />
                                    <div className="absolute bottom-[50px] z-10 flex w-full justify-center games-center">
                                        <h1 className="text-white font-bold text-2xl">{game.discount && game.discount.percent > 0 ? (getDiscount(game.publications[0].price.price, game.discount?.percent)) : (game.publications[0].price.price)} ₽</h1>
                                        {game.discount?.percent !== 0 && <Tag type="discount">-{game.discount?.percent}%</Tag>}
                                        {isNew && <Tag type="new">Новинка</Tag>}
                                    </div>
                                </Link>
                            </SwiperSlide>
                        );
                    })}
                </Swiper>
            )}
        </div>
    );
}
