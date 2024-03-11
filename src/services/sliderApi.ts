import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const sliderApi = createApi({
  reducerPath: "sliderApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:3000/" }),
  endpoints: (builder) => ({
    getSliderGames: builder.query({
      query: () => `sliderGames`,
    }),
  }),
});

export const { useGetSliderGamesQuery } = sliderApi;
