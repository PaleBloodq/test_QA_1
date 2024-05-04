import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import cookie from "cookiejs";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    headers: {
      Authorization: `Bearer ${cookie.get("token")}`,
    },
  }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: () => `api/profile/`,
    }),
    getOrders: builder.query({
      query: () => `api/profile/orders/?limit=10&offset=0`,
    }),
    makeOrder: builder.mutation({
      query: (order) => ({
        url: `api/order/buy/`,
        method: "POST",
        body: order,
      }),
    }),
    updateUserData: builder.mutation({
      query: ({ updatedData }) => ({
        url: `api/profile/update/`,
        method: "POST",
        body: updatedData,
      }),
    }),
    checkPromocode: builder.mutation({
      query: ({ promoCode }) => ({
        url: `api/order/promocode/check/`,
        method: "POST",
        body: promoCode,
      }),
    }),
    refreshToken: builder.mutation({
      query: (token) => ({
        url: `api/token/refresh/`,
        method: "POST",
        body: token,
      }),
    }),
  }),
});

export const {
  useGetUserQuery,
  useGetOrdersQuery,
  useUpdateUserDataMutation,
  useMakeOrderMutation,
  useCheckPromocodeMutation,
  useRefreshTokenMutation,
} = userApi;
