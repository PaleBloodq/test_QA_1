import Container from "../../components/common/Container";
import { useParams } from "react-router";
import { useEffect, useState } from "react";
import { useGetAnyProductQuery } from "../../services/productsApi";
import { useDispatch, useSelector } from "react-redux";
import SelectSubscription from "../../components/Subscription";
import { SubscriptionPriceType, subscriptionType } from "../../types/subscriptionType";
import { durationSelector, selectedSubscriptionSelector } from "../../features/Subscription/subscriptionSelectors";
import { setSelectedSubscription } from "../../features/Subscription/subscriptionSlice";


export default function Subscription() {

    interface RouteParams {
        [key: string]: string | undefined;
        platform: string;
        id: string;
    }

    const dispatch = useDispatch()


    const { subscriptionId, id } = useParams<RouteParams>();
    const { data = [], isLoading } = useGetAnyProductQuery(subscriptionId);
    const selectedSubscription = useSelector(selectedSubscriptionSelector);
    const currentDuration = useSelector(durationSelector);
    const [currentSubscription, setCurrentSubscription] = useState(data.durationVariations?.find((sub: subscriptionType) => sub.id === id))
    console.log(currentSubscription)
    useEffect(() => {
        setCurrentSubscription(data.durationVariations?.find((sub: subscriptionType) => sub.id === id))
        dispatch(setSelectedSubscription(data.durationVariations?.find((sub: subscriptionType) => sub.id === id).id))
    }, [data])

    useEffect(() => {
        setCurrentSubscription(data.durationVariations?.find((sub: subscriptionType) => sub.id === selectedSubscription))
    }, [selectedSubscription])

    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading && currentSubscription !== undefined ? (
                    <div className="flex flex-col items-start">
                        <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={currentSubscription.photoUrls[0]} alt="game image" />
                        <h1 className="text-header mb-2">{currentSubscription.title}</h1>
                        <div className="flex items-center">
                            <h1 className="price-big">{currentSubscription.price.find((price: SubscriptionPriceType) => price.duration === currentDuration).price} ₽</h1>
                        </div>
                        <SelectSubscription durations={data.durationVariations} />
                    </div>
                ) : (<h1>Загрузка...</h1>)
                }
            </div>
        </Container>
    )
}
