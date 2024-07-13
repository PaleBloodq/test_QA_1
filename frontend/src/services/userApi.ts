import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

function getTokenFromUrl(url: string) {
  const tokenRegex = /token=([^&#]+)/;
  const match = url.match(tokenRegex);
  if (match && match[1]) {
    sessionStorage.setItem("token", match[1]);
    return match[1];
  } else {
    return false;
  }
}

getTokenFromUrl(window.location.href);

const token = sessionStorage.getItem("token");

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: () => `api/profile/`,
    }),
    getOrders: builder.query({
      query: () => `api/profile/orders/`,
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
        body: { promoCode: promoCode },
      }),
    }),
    refreshToken: builder.mutation({
      query: (token) => ({
        url: `api/token/refresh/`,
        method: "POST",
        body: token,
      }),
    }),
    getWishlist: builder.query({
      query: () => `api/profile/wishlist/`,
    }),
    addToWishlist: builder.mutation({
      query: (id) => ({
        url: `api/profile/wishlist/`,
        method: "POST",
        body: { id: id },
      }),
    }),
    deleteFromWishlist: builder.mutation({
      query: (id) => ({
        url: `api/profile/wishlist/`,
        method: "DELETE",
        body: { id: id },
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
  useAddToWishlistMutation,
  useDeleteFromWishlistMutation,
  useGetWishlistQuery,
} = userApi;
