import { RootState } from "../../store/store";

export const currentPriceSelector = (state: RootState) => state.currentPrice.value;
