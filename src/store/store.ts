import { configureStore } from "@reduxjs/toolkit";
import { productsApi } from "../services/productsApi";
import searchSlice from "../features/Search/searchSlice";
import publicationSlice from "../features/Game/publicationSlice";
import currentPriceSlice from "../features/Game/currentPriceSlice";
import subscriptionSlice from "../features/Subscription/subscriptionSlice";
import cartSlice from "../features/Cart/cartSlice";
import userSlice from "../features/User/userSlice";

export const store = configureStore({
  reducer: {
    [productsApi.reducerPath]: productsApi.reducer,
    search: searchSlice,
    publication: publicationSlice,
    currentPrice: currentPriceSlice,
    subscription: subscriptionSlice,
    cart: cartSlice,
    user: userSlice,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware().concat(productsApi.middleware);
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
