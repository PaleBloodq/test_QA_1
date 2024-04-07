import { useDispatch, useSelector } from "react-redux";
import SubscriptionPeriodSelector from "../common/SubscriptionPeriodSelect";
import { durationSelector, selectedSubscriptionSelector } from "../../features/Subscription/subscriptionSelectors";
import { durationVariationsType } from "../../types/subscriptionType";
import { setSelectedSubscription } from "../../features/Subscription/subscriptionSlice";

export default function SelectSubscription({ durations }: { durations: durationVariationsType[] }) {

  const dispatch = useDispatch()
  const currentDuration = useSelector(durationSelector)
  const selectedSubscription = useSelector(selectedSubscriptionSelector)

  return (
    <div className="flex flex-col mt-2">
      <h1 className="text-title mb-5">Издания</h1>
      <div>
        <SubscriptionPeriodSelector selected={currentDuration} />
        <div className="w-full gap-3 flex justify-between">
          {durations.map((duration) => {
            return (
              <button
                onClick={() => dispatch(setSelectedSubscription(duration.id))}
                key={duration.id}
                className={`w-full h-20 flex flex-col justify-center items-center ${duration.id == selectedSubscription ? 'custom-border__red' : 'custom-border'}`}
              >
                <h1 className="text-subtitle">{duration.title}</h1>
                <h2 className="price-small">
                  {duration.price.find((item) => item.duration === currentDuration)?.price} ₽
                </h2>
              </button>
            )
          })}
        </div >
      </div>
    </div>
  )
}
