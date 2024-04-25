import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_DATABASE_URL }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: () => `/user`,
    }),
    getOrders: builder.query({
      query: () => `/orders`,
    }),
  }),
});

export const { useGetUserQuery, useGetOrdersQuery } = userApi;
