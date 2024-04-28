import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_DATABASE_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI4VDEyOjM0OjE3LjkwMTk5MyIsInRva2VuX3NlZWQiOiI4YjA3N2ZjMWQ3Zjc0OTc0Yjk3MzIwOThlM2MwZTU4NSJ9.oWAKw0NffeiK5XfBon3FbHmjr0ZipSbNggPMe-9P0zKiy5R-DToqH0TIhKaG-XsjM6dLtZ2O1g9FfQux28I1hhKOUgyDSvUU9lFQtkC6KwXQaFi_ch3z68oXZ_mpuhg0u4mYL0NcGJLqySaYA_PfBhfwZt6Vjq5GckuzboNUGpKmX-e6beYCdcp3f-ftzrsPHWujH0GGclQW_eTKZq9bOBbBnB7RKf-wKtkQE9FLoOuhNLaq6nXHPCt8m3EB3HeiFgbCIqG6N_Ik1Lri1qt9DceQhjHkcMbrJ7a3y7Uautxv5z5DgUo4IR9J8utek27s8OFqCKKsAyXVYBelYTX0BA`,
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
        body: { promoCode },
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
