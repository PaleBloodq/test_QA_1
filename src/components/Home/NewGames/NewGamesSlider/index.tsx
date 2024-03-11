import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import './newGamesSlider.css';
import { Pagination } from 'swiper/modules';
import { useGetSliderNewGamesQuery } from '../../../../services/sliderApi';

export default function NewGamesSlider() {

    const { data = [], isLoading } = useGetSliderNewGamesQuery({})

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
                    {data.map((game) => <div key={game.id} className='h-full'><SwiperSlide >
                        <div className='w-full h-full flex flex-col items-start justify-between'>
                            <img className='rounded-xl max-h-[200px] mb-[18px]' src={game.img} alt="game image" />
                            <h1 className='text-title text-start'>{game.name}</h1>
                            {game.publications && <h2 className='text-subtitle'>{game.publications[0].title}</h2>}
                            <h3 className='price-small'>{game.publications[0].price}</h3>
                        </div>
                    </SwiperSlide></div>)}
                </Swiper>
            }
        </>
    )
}
