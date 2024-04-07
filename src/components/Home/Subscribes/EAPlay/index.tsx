import { Link } from "react-router-dom"
import { subscriptionType } from "../../../../types/subscriptionType"
import useIsLoading from "../../../../hooks/useIsLoading"

export default function EAPlay({ data = [] }: { data: subscriptionType[] }) {

    const isLoading = useIsLoading(data[0])


    return (
        <div>
            <h1 className="text-header mb-[22px]">Подписки EA Play</h1>
            <div className="flex flex-col gap-2">
                {!isLoading && (
                    <Link to={`/subscription/${data[0].id}/${data[0].durationVariations[0].id}`} className="flex w-full px-2 py-2 custom-border justify-between items-center" key={`sub-` + data[0].id} >
                        <img src={data[0].durationVariations[0].previewImg} alt="preview" />
                        <div className="flex flex-col gap-2 items-start">
                            <h1 className="text-subtitle">{data[0].title}</h1>
                            {/* <h2 className="price-small">{subscription.durationVariations[0]} ₽</h2> */}
                        </div>
                        <div className="self-start">
                            <svg className="fill-[#606D7B] dark:fill-[#606D7B]" width="23" height="23" viewBox="0 0 23 23" xmlns=" http://www.w3.org/2000/svg">
                                <path d="M17.0106 5.16815C17.4642 5.16815 17.832 5.53592 17.832 5.98958V14.6146C17.832 15.0682 17.4642 15.436 17.0106 15.436C16.5569 15.436 16.1891 15.0682 16.1891 14.6146L16.1889 7.97169L6.33098 17.8308C6.03487 18.1269 5.56893 18.1497 5.24669 17.8992L5.1693 17.8308C4.84851 17.51 4.84851 16.9899 5.1693 16.6692L15.0265 6.81101H8.38556C7.9643 6.81101 7.6171 6.4939 7.56965 6.08538L7.56413 5.98958C7.56413 5.53592 7.93189 5.16815 8.38556 5.16815H17.0106Z" />
                            </svg>
                        </div>
                    </Link>
                )}
            </div>
        </div >
    )
}
