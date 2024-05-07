import { useEffect, useRef } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';

import 'swiper/css';
import 'swiper/css/pagination';

import './headerSlider.css';
import Tag from '../../common/Tag';
import { Link } from 'react-router-dom';
import { isNew } from '../../../hooks/useIsNew';
import useIsLoading from '../../../hooks/useIsLoading';
import { ProductType } from '../../../types/ProductType';
import { SectionType } from '../../../types/SectionType';
import { replaceUrl } from '../../../helpers/replaceUrl';

export default function HeaderSlider({ data }: { data: SectionType }) {
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
                    loop={true}
                    slidesPerView={1.2}
                    centeredSlides={true}
                    spaceBetween={13}
                    pagination={false}
                    className="headerSwiper"
                    ref={swiperRef}
                >
                    {data.objects.map((game: ProductType, index: number) => {
                        return (
                            <SwiperSlide key={`header-${index}`}>
                                <Link className="flex w-full h-full relative" to={`/game/${game.id}/${game.publications[0].id}`}>
                                    <img className="rounded-xl" src={replaceUrl(game.publications[0].preview)} alt="" />
                                    <div className="absolute bottom-[50px] z-10 flex w-full items-center gap-2 flex-col justify-center">
                                        <h1 className="font-bold text-4xl text-white drop-shadow-[0_40px_40px_rgba(1,1,1,1)]">{game.publications[0].discount && game.publications[0].discount > 0 ? (game.publications[0].final_price) : (game.publications[0].original_price)} ₽</h1>
                                        <div className='w-16 flex gap-3 justify-center'>
                                            {game.publications[0].discount !== 0 && <Tag type="discount">-{game.publications[0].discount}%</Tag>}
                                            {isNew(game.release_date) && <Tag type="new">Новинка</Tag>}
                                        </div>
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
