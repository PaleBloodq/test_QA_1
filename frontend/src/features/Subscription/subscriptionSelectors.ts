import { RootState } from "../../store/store";

export const durationSelector = (state: RootState) => state.subscription.duration;
export const selectedSubscriptionSelector = (state: RootState) =>
  state.subscription.selectedSubscription;
