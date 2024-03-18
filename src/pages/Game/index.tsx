import { useParams } from 'react-router';
import { useGetProductQuery } from '../../services/productsApi';
import { gameType } from '../../types/gameType';
import Container from '../../components/common/Container';
import Tag from '../../components/common/Tag';
import SelectPublication from '../../components/common/SelectPublictaion';
import { useDispatch, useSelector } from 'react-redux';
import { setSelectedPublication } from '../../features/Game/publicationSlice';
import { currentPriceSelector } from '../../features/Game/currentPriceSelectors';
import { setCurrentPrice } from '../../features/Game/currentPriceSlice';
import { getDiscount } from '../../hooks/getDiscount';
import { selectedPlatformSelector, selectedPublicationSelector } from '../../features/Game/publicationSelectors';
import { useEffect } from 'react';
import { Publication } from '../../types/publicationType';

export default function Game() {
    const dispatch = useDispatch();
    const { gameId } = useParams();
    const { data, isLoading, isError } = useGetProductQuery(gameId) as { data: gameType; isLoading: boolean; isError: boolean };
    const selectedPublication = useSelector(selectedPublicationSelector);
    const selectedPlatform = useSelector(selectedPlatformSelector);

    useEffect(() => {
        if (data?.publications) {
            dispatch(setSelectedPublication(data.publications[0].id));
        }
    }, [data, dispatch]);

    const currentPrice = useSelector(currentPriceSelector);

    useEffect(() => {
        const publication = data?.publications.find((pub: Publication) => pub.id === selectedPublication);
        const price = publication?.price.find((p) => p.platform === selectedPlatform)?.price;
        dispatch(setCurrentPrice(price));
    }, [selectedPublication, selectedPlatform, data]);

    if (isError) {
        return <div>Ошибка</div>;
    }

    if (isLoading) {
        return <div>Загрузка...</div>;
    }

    const { publications, photoUrls, title } = data || {};

    return (
        <Container>
            <div className="flex flex-col items-center">
                <div className="flex flex-col items-start">
                    <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={photoUrls?.[0]} alt="game image" />
                    <h1 className="text-header mb-6">{title}</h1>
                    <div className="flex items-center">
                        <h1 className="price-big">
                            {getDiscount(
                                currentPrice,
                                publications?.find((pub: Publication) => pub.id === selectedPublication)?.psPlusDiscount ||
                                publications?.find((pub: Publication) => pub.id === selectedPublication)?.discount.percent
                            )}{' '}
                            ₽
                        </h1>
                        <div className="flex">
                            {publications?.find((pub: Publication) => pub.id === selectedPublication)?.discount.percent !== 0 && (
                                <Tag type="discount">
                                    -{publications.find((pub: Publication) => pub.id === selectedPublication)?.discount.percent}%
                                </Tag>
                            )}
                        </div>
                    </div>
                    {publications?.find((pub: Publication) => pub.id === selectedPublication)?.discount.percent && (
                        <div className="w-full flex justify-between mb-5">
                            <p className="text-subtitle">Скидка действует до:</p>
                            <p className="text-subtitle-info">{publications?.find((pub: Publication) => pub.id === selectedPublication)?.discount.deadline}</p>
                        </div>
                    )}
                    <SelectPublication publications={publications} />
                </div>
            </div>
        </Container>
    );
}