import { configureStore } from "@reduxjs/toolkit";
import { productsApi } from "../services/productsApi";
import { sliderApi } from "../services/sliderApi";
import searchSlice from "../features/Search/searchSlice";

export const store = configureStore({
  reducer: {
    [productsApi.reducerPath]: productsApi.reducer,
    [sliderApi.reducerPath]: sliderApi.reducer,
    search: searchSlice,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware().concat(productsApi.middleware, sliderApi.middleware);
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
