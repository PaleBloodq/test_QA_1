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
import { isDatePassed } from '../../hooks/isDatePassed';
import ReleaseTimer from '../../components/common/ReleaseTimer';
import Line from '../../components/common/Line';
import { useGetAnyProductQuery } from '../../services/productsApi';
import { CartItemType } from '../../types/cartItem';
import AddToCartButton from '../../components/common/AddToCartButton';
import { replaceUrl } from '../../helpers/replaceUrl';
import calcCashback from '../../helpers/calcCashback';
import { ProductType } from '../../types/ProductType';

export default function Game() {
    const dispatch = useDispatch();
    const { gameId, pubId } = useParams();
    const { data = {} as ProductType, isLoading } = useGetAnyProductQuery(gameId);
    const selectedPublication = useSelector(selectedPublicationSelector);
    const selectedPlatform = useSelector(selectedPlatformSelector);
    const currentPrice = useSelector(currentPriceSelector);

    useEffect(() => {
        if (data?.publications) {
            dispatch(setSelectedPublication(data?.publications[0]?.id));
        }
    }, [data, dispatch]);

    useEffect(() => {
        dispatch(setSelectedPublication(pubId));
        const publication = data?.publications?.find(pub => pub?.id === pubId);
        if (publication) {
            dispatch(setSelectedPlatform(publication.platforms[0]));
        }
    }, [isLoading, dispatch, data, pubId]);

    useEffect(() => {
        const publication = data?.publications?.find(pub => pub?.id === selectedPublication);
        if (publication) {
            dispatch(setCurrentPrice(publication.original_price));
        }
    }, [selectedPublication, selectedPlatform, data, dispatch]);

    if (isLoading) {
        return <div>Загрузка...</div>;
    }

    const { publications, title } = data || {};
    const currentPublication = publications?.find(pub => pub?.id === selectedPublication);
    const isPsPlus = currentPublication?.ps_plus_discount;

    const cartItem: CartItemType = {
        id: currentPublication?.id,
        type: data?.type,
        img: currentPublication?.preview,
        title: data?.title,
        publication: currentPublication?.title,
        platform: selectedPlatform,
        price: currentPrice,
        final_price: currentPublication?.final_price,
        discount: currentPublication?.discount,
        cashback: currentPublication?.cashback,
    };

    const includes = currentPublication?.includes?.split("\r\n") || [];

    if (!currentPublication) {
        return <div>Publication not found</div>;
    }

    return (
        <Container>
            <div className="flex flex-col items-center">
                <div className="flex flex-col items-start w-full">
                    <img className="w-full h-[400px] rounded-xl mb-8 object-cover" src={replaceUrl(currentPublication?.photo)} alt="game image" />
                    <div className='flex items-center mb-2 gap-2'>
                        <h1 className="text-header">{title && title}</h1>
                        {isNew(data?.release_date) && <Tag type="new">Новинка</Tag>}
                    </div>
                    <div className="flex items-center flex-wrap w-full gap-2">
                        {!isPsPlus ? (
                            <h1 className="price-big">
                                {currentPublication?.final_price || 0} ₽
                            </h1>
                        ) : (
                            <SelectPrice price={currentPrice} discount={currentPublication?.ps_plus_discount} />
                        )}
                        <div className="flex gap-2">
                            {currentPublication?.ps_plus_discount === 0 && currentPublication?.discount > 0 ? (
                                <Tag type="discount">-{currentPublication.discount}%</Tag>
                            ) : null}
                            {currentPublication?.cashback ? <Tag type="cashback">Кэшбэк: {calcCashback(currentPrice, currentPublication?.cashback)} ₽</Tag> : null}
                        </div>
                    </div>
                    {currentPublication?.discount ? (
                        <div className="w-full flex justify-between mb-5">
                            <p className="text-subtitle">Скидка действует до:</p>
                            <p className="text-subtitle-info">{currentPublication?.discount_deadline}</p>
                        </div>
                    ) : null}
                    <SelectPublication publications={publications} />
                    {!isDatePassed(data?.release_date) && <ReleaseTimer releaseDate={data?.release_date} />}
                    <Line />
                    {includes?.length > 1 &&
                        <>
                            <div className='flex flex-col'>
                                <h1 className='text-title-xl mb-[20px]'>Состав издания:</h1>
                                <ul className='list-disc ml-3'>
                                    {includes?.length && includes?.map((item: ReactNode, index: number) => (
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
                            <p className='text-title text-[14px]'>{currentPublication?.platforms.map((platform) => platform)?.join(', ')}</p>
                        </div>
                        <div className='w-full flex justify-between'>
                            <p className='text-subtitle'>Язык:</p>
                            <p className='text-title text-[14px]'>{data?.languages?.map((lang) => lang)?.join(', ')}</p>
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