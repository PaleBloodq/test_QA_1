import { configureStore } from "@reduxjs/toolkit";
import { productsApi } from "../services/productsApi";
import { userApi } from "../services/userApi";
import searchSlice from "../features/Search/searchSlice";
import publicationSlice from "../features/Game/publicationSlice";
import currentPriceSlice from "../features/Game/currentPriceSlice";
import subscriptionSlice from "../features/Subscription/subscriptionSlice";
import cartSlice from "../features/Cart/cartSlice";
import userSlice from "../features/User/userSlice";
import { cartApi } from "../services/cartApi";

export const store = configureStore({
  reducer: {
    [productsApi.reducerPath]: productsApi.reducer,
    [userApi.reducerPath]: userApi.reducer,
    [cartApi.reducerPath]: cartApi.reducer,
    search: searchSlice,
    publication: publicationSlice,
    currentPrice: currentPriceSlice,
    subscription: subscriptionSlice,
    cart: cartSlice,
    user: userSlice,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware().concat(
      productsApi.middleware,
      userApi.middleware,
      cartApi.middleware
    );
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
