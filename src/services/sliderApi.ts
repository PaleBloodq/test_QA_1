import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const sliderApi = createApi({
  reducerPath: "sliderApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_DATABASE_URL }),
  endpoints: (builder) => ({
    getSliderGames: builder.query({
      query: () => `offers`,
    }),
    getSliderNewGames: builder.query({
      query: () => `new`,
    }),
    getSliderLeadersGames: builder.query({
      query: () => `leaders`,
    }),
    getSliderDonations: builder.query({
      query: () => `donation`,
    }),
  }),
});

export const {
  useGetSliderGamesQuery,
  useGetSliderNewGamesQuery,
  useGetSliderLeadersGamesQuery,
  useGetSliderDonationsQuery,
} = sliderApi;
