import { useEffect, useRef } from 'react';
import { useGetSliderGamesQuery } from "../../../services/sliderApi"
import { Swiper, SwiperSlide } from 'swiper/react';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/pagination';

import './headerSlider.css';

export default function HeaderSlider() {
    const { data = [], isLoading } = useGetSliderGamesQuery({})
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
            {!isLoading &&

                <Swiper
                    slidesPerView={"auto"}
                    centeredSlides={true}
                    spaceBetween={13}
                    pagination={false}
                    className="headerSwiper"
                    ref={swiperRef}
                >
                    {data.map((item) => {
                        return (
                            <SwiperSlide key={item.id}>
                                <div className='flex w-full h-full relative'>
                                    <img className='rounded-xl' src={item.img} alt="" />
                                    <div className='absolute bottom-[50px] z-10 flex w-full justify-center'>
                                        <h1 className='text-white font-bold text-2xl'>{item.publications[0].price}</h1>
                                        <h2 className='ml-4 text-[14px] px-[6px] bg-discount rounded-xl font-extrabold text-[#2C0C11] flex items-center justify-center'>{item.tags[0]}</h2>
                                    </div>
                                </div>
                            </SwiperSlide>
                        )
                    })}
                </Swiper>
            }
        </div>
    )
}