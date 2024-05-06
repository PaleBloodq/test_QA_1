import SubscriptionPeriodSelector from "../../../common/SubscriptionPeriodSelect"
import { Link } from "react-router-dom";
import useIsLoading from "../../../../hooks/useIsLoading";
import { useSelector } from "react-redux";
import { durationSelector } from "../../../../features/Subscription/subscriptionSelectors";
import { ProductType } from "../../../../types/ProductType";
import { Publication } from "../../../../types/PublicationType";
import { replaceUrl } from "../../../../helpers/replaceUrl";

export default function PSPlus({ data = [] }: { data: ProductType[] }) {
    const isLoading = useIsLoading(data[0])
    const duration = useSelector(durationSelector)

    const groupedSubscriptions = data[0]?.publications.reduce((acc: any, sub: any) => {
        if (!acc[sub.title]) {
            acc[sub.title] = [];
        }
        acc[sub.title].push(sub);
        return acc;
    }, {});


    return (
        <div>
            <h1 className="text-header mb-[22px]">Подписки PS Plus</h1>
            <SubscriptionPeriodSelector selected={duration} />
            <div className="flex flex-col gap-2">
                {!isLoading && groupedSubscriptions && Object.entries(groupedSubscriptions).map((subscription: any, index: number) => {
                    return (
                        <Link to={`/subscription/${data[0]?.id}/${subscription[1].find((pub: Publication) => pub.duration === duration)?.id}`} className="flex w-full px-2 py-2 custom-border justify-between items-center" key={'pssub-' + index}>
                            <img className="max-w-[111px] max-h-[80px]" src={replaceUrl(subscription[1]?.find((pub: Publication) => pub.duration === duration)?.preview)} alt="preview" />
                            <div className="flex flex-col gap-2 items-start">
                                <h1 className="text-subtitle">{subscription[0]}</h1>
                                <h2 className="price-small">{subscription[1]?.find((pub: Publication) => pub.duration === duration)?.original_price} ₽</h2>
                            </div>
                            <div className="self-start">
                                <svg className="fill-[#606D7B] dark:fill-[#606D7B]" width="23" height="23" viewBox="0 0 23 23" xmlns=" http://www.w3.org/2000/svg">
                                    <path d="M17.0106 5.16815C17.4642 5.16815 17.832 5.53592 17.832 5.98958V14.6146C17.832 15.0682 17.4642 15.436 17.0106 15.436C16.5569 15.436 16.1891 15.0682 16.1891 14.6146L16.1889 7.97169L6.33098 17.8308C6.03487 18.1269 5.56893 18.1497 5.24669 17.8992L5.1693 17.8308C4.84851 17.51 4.84851 16.9899 5.1693 16.6692L15.0265 6.81101H8.38556C7.9643 6.81101 7.6171 6.4939 7.56965 6.08538L7.56413 5.98958C7.56413 5.53592 7.93189 5.16815 8.38556 5.16815H17.0106Z" />
                                </svg>
                            </div>
                        </Link>
                    )
                })}
            </div>
        </div >
    )
}
