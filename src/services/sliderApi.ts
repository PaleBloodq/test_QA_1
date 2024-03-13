import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const sliderApi = createApi({
  reducerPath: "sliderApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:3000/" }),
  endpoints: (builder) => ({
    getSliderGames: builder.query({
      query: () => `offers`,
    }),
    getSliderNewGames: builder.query({
      query: () => `new`,
    }),
  }),
});

export const { useGetSliderGamesQuery, useGetSliderNewGamesQuery } = sliderApi;
