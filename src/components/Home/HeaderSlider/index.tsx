import { useEffect, useRef } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { getDiscount } from '../../../hooks/getDiscount';

import 'swiper/css';
import 'swiper/css/pagination';

import './headerSlider.css';
import Tag from '../../common/Tag';
import { GameType } from '../../../types/gameType';
import { Link } from 'react-router-dom';
import { isNew } from '../../../hooks/useIsNew';
import useIsLoading from '../../../hooks/useIsLoading';

export default function HeaderSlider({ data }: { data: GameType[] }) {
    const swiperRef = useRef(null);
    const isLoading = useIsLoading(data)
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
                    {data.map((game: GameType, index: number) => {
                        return (
                            <SwiperSlide key={`header-${index}`}>
                                <Link className="flex w-full h-full relative" to={"/game/" + game.id}>
                                    <img className="rounded-xl" src={game.previewImg} alt="" />
                                    <div className="absolute bottom-[50px] z-10 flex w-full justify-center items-center gap-2">
                                        <h1 className="text-white font-bold text-2xl">{game.publications[0].discount.percent && game.publications[0].discount.percent > 0 ? (getDiscount(game.publications[0].price[0].price, game.publications[0].discount.percent)) : (game.publications[0].price[0].price)} ₽</h1>
                                        {game.publications[0].discount.percent !== 0 && <Tag type="discount">-{game.publications[0].discount.percent}%</Tag>}
                                        {isNew(game.releaseDate) && <Tag type="new">Новинка</Tag>}
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
