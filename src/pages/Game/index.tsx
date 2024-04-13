import { ReactNode, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router';
import Container from '../../components/common/Container';
import SelectPublication from '../../components/common/SelectPublictaion';
import SelectPrice from '../../components/common/SelectPrice';
import Tag from '../../components/common/Tag';
import { currentPriceSelector } from '../../features/Game/currentPriceSelectors';
import { setCurrentPrice } from '../../features/Game/currentPriceSlice';
import { setSelectedPublication } from '../../features/Game/publicationSlice';
import { selectedPlatformSelector, selectedPublicationSelector } from '../../features/Game/publicationSelectors';
import { PriceType, Publication } from '../../types/publicationType';
import { isNew } from '../../hooks/useIsNew';
import { getDiscount } from '../../hooks/getDiscount';
import { isDatePassed } from '../../hooks/isDatePassed';
import ReleaseTimer from '../../components/common/ReleaseTimer';
import Line from '../../components/common/Line';
import { useGetAnyProductQuery } from '../../services/productsApi';
import { CartItemType } from '../../types/cartItem';
import AddToCartButton from '../../components/common/AddToCartButton';

export default function Game() {
    const dispatch = useDispatch();
    const { gameId } = useParams();
    const { data = [], isLoading } = useGetAnyProductQuery(gameId);
    const selectedPublication = useSelector(selectedPublicationSelector);
    const selectedPlatform = useSelector(selectedPlatformSelector);
    const currentPrice = useSelector(currentPriceSelector);


    useEffect(() => {
        if (data?.publications) {
            dispatch(setSelectedPublication(data.publications[0].id));
        }
    }, [data, dispatch]);

    useEffect(() => {
        const publication = data?.publications?.find((pub: Publication) => pub.id === selectedPublication);
        const price = publication?.price.find((p: PriceType) => p.platform === selectedPlatform)?.price;
        dispatch(setCurrentPrice(price));
    }, [selectedPublication, selectedPlatform, data]);


    if (isLoading) {
        return <div>Загрузка...</div>;
    }

    const { publications, photoUrls, title } = data || {};
    const currentPublication = publications?.find((pub: Publication) => pub.id === selectedPublication);
    const isPsPlus = currentPublication?.psPlusDiscount;


    const cartItem: CartItemType = {
        id: currentPublication?.id,
        type: data?.type,
        img: data?.previewImg,
        title: data?.title,
        publication: currentPublication?.title,
        platform: selectedPlatform,
        price: currentPrice,
        discount: currentPublication?.discount.percent,
        cashback: currentPublication?.cashback
    }

    return (
        <Container>
            <div className="flex flex-col items-center">
                <div className="flex flex-col items-start">
                    <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={photoUrls?.[0]} alt="game image" />
                    <div className='flex items-center mb-2 gap-2'>
                        <h1 className="text-header">{title}</h1>
                        {isNew(data.releaseDate) && <Tag type="new">Новинка</Tag>}
                    </div>
                    <div className="flex items-center flex-wrap w-full gap-2">
                        {!isPsPlus ? (
                            <h1 className="price-big">
                                {getDiscount(currentPrice, currentPublication?.psPlusDiscount || currentPublication?.discount.percent || 0)} ₽
                            </h1>
                        ) : (
                            <SelectPrice price={currentPrice} discount={currentPublication.psPlusDiscount} />
                        )}
                        <div className="flex gap-2">
                            {currentPublication?.psPlusDiscount === 0 && currentPublication?.discount.percent ? (
                                <Tag type="discount">-{currentPublication.discount.percent}%</Tag>
                            ) : null}
                            {currentPublication?.cashback ? <Tag type="cashback">Кэшбэк: {currentPublication.cashback}₽</Tag> : null}
                        </div>
                    </div>
                    {currentPublication?.discount.percent ? (
                        <div className="w-full flex justify-between mb-5">
                            <p className="text-subtitle">Скидка действует до:</p>
                            <p className="text-subtitle-info">{currentPublication.discount.deadline}</p>
                        </div>
                    ) : null}
                    <SelectPublication publications={publications} />
                    {!isDatePassed(data.releaseDate) && <ReleaseTimer releaseDate={data.releaseDate} />}
                    <Line />
                    <div className='flex flex-col px-3'>
                        <h1 className='text-title-xl mb-[20px]'>Состав издания:</h1>
                        <ul className='list-disc'>
                            {currentPublication?.includes.map((item: ReactNode, index: number) => (
                                <li key={index} className='custom-marker text-subtitle'>{item}</li>
                            ))}
                        </ul>
                    </div>
                    <Line />
                    <div className='flex flex-col gap-2 w-full'>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Платформа:</p>
                            <p className='text-title text-[14px]'>{data.platforms.map((platform: string[]) => platform).join(', ')}</p>
                        </div>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Язык:</p>
                            <p className='text-title text-[14px]'>{data.languages.map((lang: string[]) => lang).join(', ')}</p>
                        </div>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Дата релиза:</p>
                            <p className='text-title text-[14px]'>{data.releaseDate}</p>
                        </div>
                    </div>
                    <AddToCartButton cartItem={cartItem} />
                </div>
            </div>
        </Container>
    );
}
