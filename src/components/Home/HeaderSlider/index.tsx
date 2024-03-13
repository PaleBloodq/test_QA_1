import { useEffect, useRef } from 'react';
import { useGetSliderGamesQuery } from "../../../services/sliderApi"
import { differenceInMonths, parseISO } from 'date-fns';
import { Swiper, SwiperSlide } from 'swiper/react';

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
                    {data.map((item: gameType, index: number) => {
                        const releaseDate = parseISO(item.releaseDate);
                        const isNew = differenceInMonths(new Date(), releaseDate) < 2;

                        return (
                            <SwiperSlide key={`header-${index}`}>
                                <Link className="flex w-full h-full relative" to={"/game/" + item.id}>
                                    <img className="rounded-xl" src={item.previewImg} alt="" />
                                    <div className="absolute bottom-[50px] z-10 flex w-full justify-center items-center">
                                        <h1 className="text-white font-bold text-2xl">{item.publications[0].price}</h1>
                                        {item.discount?.percent !== 0 && <Tag type="discount">-{item.discount?.percent}%</Tag>}
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
