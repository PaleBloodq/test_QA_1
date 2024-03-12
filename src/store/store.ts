import { configureStore } from "@reduxjs/toolkit";
import { productsApi } from "../services/productsApi";
import { sliderApi } from "../services/sliderApi";
import searchSlice from "../features/Search/searchSlice";
import { subscribesApi } from "../services/subscribesApi";

export const store = configureStore({
  reducer: {
    [productsApi.reducerPath]: productsApi.reducer,
    [sliderApi.reducerPath]: sliderApi.reducer,
    [subscribesApi.reducerPath]: subscribesApi.reducer,
    search: searchSlice,
  },
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware().concat(
      productsApi.middleware,
      sliderApi.middleware,
      subscribesApi.middleware
    );
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
