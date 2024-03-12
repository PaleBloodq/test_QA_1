import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const subscribesApi = createApi({
  reducerPath: "subscribesApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:3000/" }),
  endpoints: (builder) => ({
    getSubscribes: builder.query({
      query: () => `subscribes`,
    }),
    getPsSubscribes: builder.query({
      query: () => `subscribes/psPlus`,
    }),
    getEaSubscribes: builder.query({
      query: () => `subscribes/eaPlay`,
    }),
  }),
});

export const { useGetSubscribesQuery, useGetPsSubscribesQuery, useGetEaSubscribesQuery } =
  subscribesApi;
