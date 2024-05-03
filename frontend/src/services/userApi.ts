import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MjM0MjMsInRva2VuX2V4cGlyYXRvbiI6IjIwMjQtMDUtMDJUMjI6Mjc6MTcuOTU3NDQ4IiwidG9rZW5fc2VlZCI6IjllZDJiOWI3YzVkMzQxODVhZGMxNTU4ODhkNTJmMzJmIn0.vt0pZJUwNCLvQs8DG5FLPWdjynMX0P7aXkoHo5JGxSgVlNd5Q0qkby0X986-4gnd2zrNzBHGSYzdxdpsnIj880qZSoHCtixaNH32JosQopjW4LJugtvKQMkxrbbQDwU-9wjU1ptDp_ezFAWDa_U53QcRtbweAkQDfG_TRkYfH0RPOHn9eJ8b8vdTYYyXC5LGLIAQYRFDrAToI3gCvcoAs1vjTJ7bgOPuobgYKWWEM1vy0Qf2_I7OJekwompIi0AlgLsbfhQNKGkPAwvIkXihCKglBM9XGRBiThHjEyySUcu_ig05snUWO7-N6RGaZMxbHnm_ynQqyzBHIYz5yl40-Q`,
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
