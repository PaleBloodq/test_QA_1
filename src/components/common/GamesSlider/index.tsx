import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import './newGamesSlider.css';
import { Pagination } from 'swiper/modules';
import Tag from '../Tag';
import { gameType } from '../../../types/gameType';
import { Link } from 'react-router-dom';
import { getDiscount } from '../../../hooks/getDiscount';

type GamesSliderProps = {
    data: gameType[],
    isLoading: boolean,
}

export default function GamesSlider({ data, isLoading }: GamesSliderProps) {
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
                    {data.map((game: gameType, index: number) => <div key={index} className='h-full'><SwiperSlide >
                        <Link to={'/game/' + game.id} className='w-full h-full flex flex-col items-start justify-between'>
                            <img className='rounded-xl max-h-[200px] mb-[18px]' src={game.previewImg} alt="game image" />
                            <h1 className='text-title text-start'>{game.title}</h1>
                            {game.publications && <h2 className='text-subtitle'>{game.publications[0].title}</h2>}
                            <div className='flex gap-1'>
                                <h3 className='price-small'>{game.discount && game.discount.percent > 0 ? (getDiscount(game.publications[0].price[0].price, game.discount?.percent)) : (game.publications[0].price[0].price)} ₽</h3>
                                {game.discount?.percent !== 0 && <Tag type="discount">-{game.discount?.percent}%</Tag>}
                            </div>
                        </Link>
                    </SwiperSlide></div>)}
                </Swiper>
            }
        </>
    )
}
