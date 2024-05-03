import { useDispatch, useSelector } from "react-redux";
import SubscriptionPeriodSelector from "../common/SubscriptionPeriodSelect";
import { durationSelector, selectedSubscriptionSelector } from "../../features/Subscription/subscriptionSelectors";
import { setSelectedSubscription } from "../../features/Subscription/subscriptionSlice";
import { Publication } from "../../types/PublicationType";
import { useEffect } from "react";

export default function SelectSubscription({ publications }: { publications: Publication[] }) {

  const dispatch = useDispatch()
  const currentDuration = useSelector(durationSelector)
  const selectedSubscription = useSelector(selectedSubscriptionSelector)

  const filteredPublications = publications?.filter((pub) => pub.duration === currentDuration)

  useEffect(() => {
    dispatch(setSelectedSubscription(filteredPublications.find((item) => item.duration === currentDuration)?.id))
  }, [currentDuration])

  return (
    <div className="flex flex-col mt-2">
      <h1 className="text-title mb-5">Издания</h1>
      <div>
        <SubscriptionPeriodSelector selected={currentDuration} />
        {filteredPublications.length > 1 &&
          <div className="w-full gap-3 flex justify-center flex-wrap">
            {filteredPublications.map((pub) => {
              return (
                <button
                  onClick={() => dispatch(setSelectedSubscription(pub.id))}
                  key={pub.id}
                  className={`w-[107px] h-20 flex flex-col justify-center items-center ${pub.id == selectedSubscription ? 'custom-border__red' : 'custom-border'}`}
                >
                  <h1 className="text-subtitle">{pub.title}</h1>
                  <h2 className="price-small">
                    {pub.original_price} ₽
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
