import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI5VDIxOjMzOjUzLjUxMjAxOSIsInRva2VuX3NlZWQiOiI1ZDRmOWUxMGI5ODI0ZjQ0YTcwNWMyZGFlNzQwYTE2ZCJ9.FmN4_ZYniAncitgMQZwtTnj9JhEWrtJUVpkBuHDAistrNXYEBNIWzh6PuYuMYalxX_AepJqEyL8O11ODImoZsJFX2z_zXt0H5aBzaiXEI6CiWTaHVnK7UnU8fo4wzNPsMGAPfrD8QrJBVv7QsYqXpF2XT1SgAopZCRx_4NodSc-8RnbVP2G-SIMhgzFq9qvMS1SvRrxEaEgLXdOgbSCFm4O5yyzy7GfCiFG9ct1AV48QVXA0CRgS4-_NMOSr83PQzHNq-5Lk8sKAKgyYhcsjZr28r_2v8QXkHG-aZclXgj4bPvCXei10XFaQRpmRYmJcnxDVrJTlw6gbZ-7u5fquMg`,
    },
  }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: () => `profile/`,
    }),
    getOrders: builder.query({
      query: () => `profile/orders/?limit=10&offset=0`,
    }),
    makeOrder: builder.mutation({
      query: (order) => ({
        url: `/order/buy/`,
        method: "POST",
        body: order,
      }),
    }),
    updateUserData: builder.mutation({
      query: ({ updatedData }) => ({
        url: `profile/update/`,
        method: "POST",
        body: updatedData,
      }),
    }),
    checkPromocode: builder.mutation({
      query: ({ promoCode }) => ({
        url: `order/promocode/check/`,
        method: "POST",
        body: promoCode,
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
} = userApi;
