import { ReactNode, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router';
import Container from '../../components/common/Container';
import SelectPublication from '../../components/common/SelectPublictaion';
import SelectPrice from '../../components/common/SelectPrice';
import Tag from '../../components/common/Tag';
import { currentPriceSelector } from '../../features/Game/currentPriceSelectors';
import { setCurrentPrice } from '../../features/Game/currentPriceSlice';
import { setSelectedPlatform, setSelectedPublication } from '../../features/Game/publicationSlice';
import { selectedPlatformSelector, selectedPublicationSelector } from '../../features/Game/publicationSelectors';
import { isNew } from '../../hooks/useIsNew';
import { getDiscount } from '../../hooks/getDiscount';
import { isDatePassed } from '../../hooks/isDatePassed';
import ReleaseTimer from '../../components/common/ReleaseTimer';
import Line from '../../components/common/Line';
import { useGetAnyProductQuery } from '../../services/productsApi';
import { CartItemType } from '../../types/cartItem';
import AddToCartButton from '../../components/common/AddToCartButton';
import { Publication } from '../../types/PublicationType';
import { replaceUrl } from '../../helpers/replaceUrl';
import { ProductType } from '../../types/ProductType';
import calcCashback from '../../helpers/calcCashback';

export default function Game() {
    const dispatch = useDispatch();
    const { gameId, pubId } = useParams();
    const { data = [] as ProductType, isLoading } = useGetAnyProductQuery(gameId);
    const selectedPublication = useSelector(selectedPublicationSelector);
    const selectedPlatform = useSelector(selectedPlatformSelector);
    const currentPrice = useSelector(currentPriceSelector);


    useEffect(() => {
        if (data?.publications) {
            dispatch(setSelectedPublication(data.publications[0].id));
        }
    }, [data, dispatch]);

    useEffect(() => {
        dispatch(setSelectedPublication(pubId))
        dispatch(setSelectedPlatform(data?.publications?.find((pub) => pub.id === pubId).platforms[0]));
    }, [isLoading])

    useEffect(() => {
        const publication = data?.publications?.find((pub: Publication) => pub.id === selectedPublication);
        const price = publication?.price
        dispatch(setCurrentPrice(price));
    }, [selectedPublication, selectedPlatform, data]);


    if (isLoading) {
        return <div>Загрузка...</div>;
    }

    const { publications, title } = data || {};
    const currentPublication = publications?.find((pub: Publication) => pub.id === selectedPublication);
    const isPsPlus = currentPublication?.ps_plus_discount;



    const cartItem: CartItemType = {
        id: currentPublication?.id,
        type: data?.type,
        img: currentPublication?.preview,
        title: data?.title,
        publication: currentPublication?.title,
        platform: selectedPlatform,
        price: currentPrice,
        discount: currentPublication?.discount,
        cashback: currentPublication?.cashback
    }

    const includes = currentPublication?.includes?.split("\r\n") || []



    return (
        <Container>
            <div className="flex flex-col items-center">
                <div className="flex flex-col items-start">
                    <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={replaceUrl(currentPublication?.photo)} alt="game image" />
                    <div className='flex items-center mb-2 gap-2'>
                        <h1 className="text-header">{title}</h1>
                        {isNew(data.release_date) && <Tag type="new">Новинка</Tag>}
                    </div>
                    <div className="flex items-center flex-wrap w-full gap-2">
                        {!isPsPlus ? (
                            <h1 className="price-big">
                                {getDiscount(currentPrice, currentPublication?.ps_plus_discount || currentPublication?.discount || 0)} ₽
                            </h1>
                        ) : (
                            <SelectPrice price={currentPrice} discount={currentPublication.ps_plus_discount} />
                        )}
                        <div className="flex gap-2">
                            {currentPublication?.ps_plus_discount === null && currentPublication?.discount > 0 ? (
                                <Tag type="discount">-{currentPublication.discount}%</Tag>
                            ) : null}
                            {currentPublication?.cashback ? <Tag type="cashback">Кэшбэк: {calcCashback(currentPrice, currentPublication.cashback)} ₽</Tag> : null}
                        </div>
                    </div>
                    {currentPublication?.discount ? (
                        <div className="w-full flex justify-between mb-5">
                            <p className="text-subtitle">Скидка действует до:</p>
                            <p className="text-subtitle-info">{currentPublication.discount_deadline}</p>
                        </div>
                    ) : null}
                    <SelectPublication publications={publications} />
                    {!isDatePassed(data.release_date) && <ReleaseTimer releaseDate={data.release_date} />}
                    <Line />
                    {includes.length > 1 &&
                        <>
                            <div className='flex flex-col'>
                                <h1 className='text-title-xl mb-[20px]'>Состав издания:</h1>
                                <ul className='list-disc ml-3'>
                                    {includes.length && includes.map((item: ReactNode, index: number) => (
                                        <li key={index} className='custom-marker text-subtitle'>{item}</li>
                                    ))}
                                </ul>
                            </div>
                            <Line />
                        </>
                    }
                    <div className='flex flex-col gap-2 w-full'>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Платформа:</p>
                            <p className='text-title text-[14px]'>{currentPublication?.platforms.map((platform) => platform).join(', ')}</p>
                        </div>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Язык:</p>
                            <p className='text-title text-[14px]'>{data?.languages.map((lang) => lang).join(', ')}</p>
                        </div>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Дата релиза:</p>
                            <p className='text-title text-[14px]'>{data?.release_date}</p>
                        </div>
                    </div>
                    <AddToCartButton cartItem={cartItem} />
                </div>
            </div>
        </Container>
    );
}
