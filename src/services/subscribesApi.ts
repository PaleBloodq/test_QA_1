import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const subscribesApi = createApi({
  reducerPath: "subscribesApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_DATABASE_URL }),
  endpoints: (builder) => ({
    getSubscribes: builder.query({
      query: () => `subscribes`,
    }),
    getPsSubscribes: builder.query({
      query: () => `psPlus`,
    }),
    getEaSubscribes: builder.query({
      query: () => `eaPlay`,
    }),
    getEaSubscribe: builder.query({
      query: (id) => `eaPlay/${id}`,
    }),
    getPsSubscribe: builder.query({
      query: (id) => `psPlus/${id}`,
    }),
    getSubscribe: builder.query({
      query: (info: string) => {
        const infoArray = info.split(" ");
        const platform = infoArray[0];
        const id = infoArray[1];
        if (platform === "ps") {
          return `psPlus/${id}`;
        } else {
          return `eaPlay/${id}`;
        }
      },
    }),
  }),
});

export const {
  useGetSubscribesQuery,
  useGetPsSubscribesQuery,
  useGetEaSubscribesQuery,
  useGetEaSubscribeQuery,
  useGetPsSubscribeQuery,
  useGetSubscribeQuery,
} = subscribesApi;
