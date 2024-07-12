import { useDispatch, useSelector } from "react-redux";
import SubscriptionPeriodSelector from "../common/SubscriptionPeriodSelect";
import { durationSelector, selectedSubscriptionSelector } from "../../features/Subscription/subscriptionSelectors";
import { setSelectedSubscription } from "../../features/Subscription/subscriptionSlice";
import { PublicationType } from "../../types/publicationType";
import { useEffect } from "react";

export default function SelectSubscription({ publications }: { publications: PublicationType[] }) {

  const dispatch = useDispatch()
  const currentDuration = useSelector(durationSelector)
  const selectedSubscription = useSelector(selectedSubscriptionSelector)

  const currentDurationPublications = publications?.filter((pub) => pub.duration === currentDuration)

  useEffect(() => {
    const currentSubItem = publications?.find((item) => item.id === selectedSubscription)
    dispatch(setSelectedSubscription(currentDurationPublications?.find(item => item.title === currentSubItem?.title)?.id))
  }, [currentDurationPublications])

  return (
    <div className="flex flex-col mt-2 w-full mx-auto">
      <h1 className="text-title mb-5">Издания</h1>
      <div>
        <SubscriptionPeriodSelector selected={currentDuration} />
        {currentDurationPublications.length > 1 &&
          <div className="w-full gap-3 flex justify-center flex-wrap">
            {currentDurationPublications.map((pub) => {
              return (
                <button
                  onClick={() => dispatch(setSelectedSubscription(pub.id))}
                  key={pub.id}
                  className={`w-[107px] h-20 flex flex-col justify-center items-center ${pub.id == selectedSubscription ? 'custom-border__red' : 'custom-border'}`}
                >
                  <h1 className="text-subtitle">{pub.title}</h1>
                  <h2 className="price-small">
                    {pub.final_price} ₽
                  </h2>
                </button>
              )
            })}
          </div >
        }
      </div>
    </div>
  )
}
