import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_DATABASE_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI3VDE5OjIzOjQ3Ljc3NjY2OSIsInRva2VuX3NlZWQiOiJhNGFjOTc0NDAzMWU0YTY0OTkzZGQyNzg0ODJiOWY5ZSJ9.Ql8fFu0Wz-KjoU8oV3EeZiW134SHFfoV2fquprQoWPttG0-wFlplDqWJtsWJRvqgubrNrFjHWUtg_7NKUvyEiUE5AoB18r0RaRAHcj9Qd9lVPwiM7vpqj_FDVvWWljQmCeleiVKjjYt9Ty2SaPlaKbRyQ28K4IcQDaeh6fovxhfp0HJG-wULFgaJ0Z7nSdKtHsioHVyhSsYrvlEF7gkUzGzw9gDYOcREfauigVE5eTHp2zXwiheZpyhhvFgPQM-LXh6H-UN1vAyDMN_Qi7tNX5pAqia_cnalxRsJZxkGu1XzqLrL4AGgP5MQLUe4n-wm2Nv_lnTKXyB4AcDCP5vQdw`,
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
        url: `/order/buy`,
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
