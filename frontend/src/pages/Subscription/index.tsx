import Container from "../../components/common/Container";
import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { useGetAnyProductQuery } from "../../services/productsApi";
import { useDispatch, useSelector } from "react-redux";
import SelectSubscription from "../../components/Subscription";
import { durationSelector, selectedSubscriptionSelector } from "../../features/Subscription/subscriptionSelectors";
import { setDuration, setSelectedSubscription } from "../../features/Subscription/subscriptionSlice";
import Line from "../../components/common/Line";
import { CartItemType } from "../../types/cartItem";
import AddToCartButton from "../../components/common/AddToCartButton";
import { Publication } from "../../types/PublicationType";
import { replaceUrl } from "../../helpers/replaceUrl";
import { ProductType } from "../../types/ProductType";


export default function Subscription() {

    interface RouteParams {
        [key: string]: string | undefined;
        platform: string;
        id: string;
    }

    const dispatch = useDispatch()


    const { subscriptionId, id } = useParams<RouteParams>();
    const { data = {} as ProductType, isLoading } = useGetAnyProductQuery(subscriptionId);
    const selectedSubscription = useSelector(selectedSubscriptionSelector);
    const currentDuration = useSelector(durationSelector);
    const [currentSubscription, setCurrentSubscription] = useState(data?.publications?.find((sub: Publication) => sub?.id === id))

    useEffect(() => {
        setCurrentSubscription(data?.publications?.find((sub: Publication) => sub?.id === selectedSubscription))
    }, [selectedSubscription])


    const currentPrice = currentSubscription?.original_price



    const cartItem: CartItemType = {
        id: currentSubscription?.id,
        type: "SUBSCRIPTION",
        img: currentSubscription?.preview,
        title: data?.title?.includes('PS') ? `PS Plus ${currentSubscription?.title}` : `EA Play ${currentSubscription?.title}`,
        publication: `${currentDuration} мес`,
        platform: data?.title?.includes('PS') ? 'PS' : "EA",
        price: currentPrice,
        discount: currentSubscription?.discount,
        cashback: currentSubscription?.cashback
    }

    useEffect(() => {
        if (!isLoading) {
            dispatch(setSelectedSubscription(id))
            dispatch(setDuration(data?.publications?.find((sub: Publication) => sub?.id === id)?.duration))
        }
    }, [isLoading])

    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading && currentSubscription !== undefined ? (
                    <div className="flex flex-col items-start w-full">
                        <img className="w-full h-[400px] rounded-xl mb-8 object-cover" src={replaceUrl(currentSubscription?.photo)} alt="subscription image" />
                        <h1 className="text-header mb-2">{data?.title.includes('PS') ? 'PS Plus' : 'EA Play'} {currentSubscription?.title}</h1>
                        <div className="flex items-center">
                            <h1 className="price-big">{currentPrice} ₽</h1>
                        </div>
                        <SelectSubscription publications={data?.publications} />
                        <div className="mt-8 w-full">
                            <p className="text-subtitle-info">
                                {currentSubscription?.includes}
                            </p>
                        </div>
                        <Line />
                        <div className='flex flex-col gap-2 w-full'>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Платформа:</p>
                                <p className='text-title text-[14px]'>{currentSubscription?.platforms?.map((platform) => platform).join(', ')}</p>
                            </div>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Язык:</p>
                                <p className='text-title text-[14px]'>{data?.languages?.map((lang) => lang).join(', ')}</p>
                            </div>
                            <div className='w-full flex justify-between'>
                                <p className='text-subtitle'>Дата релиза:</p>
                                <p className='text-title text-[14px]'>{data?.release_date || 'Нет данных'}</p>
                            </div>
                        </div>
                        <AddToCartButton cartItem={cartItem} />
                    </div>
                ) : (<h1>Загрузка...</h1>)
                }
            </div>
        </Container>
    )
}
