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

export const cartApi = createApi({
  reducerPath: "cartApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }),
  endpoints: (builder) => ({
    getCart: builder.query({
      query: () => "/api/cart/",
    }),
    addToCart: builder.mutation({
      query: (body) => ({
        url: "/api/cart/",
        method: "POST",
        body,
      }),
    }),
    removeFromCart: builder.mutation({
      query: (body) => ({
        url: "/api/cart/",
        method: "DELETE",
        body,
      }),
    }),
  }),
});
export const { useGetCartQuery, useAddToCartMutation, useRemoveFromCartMutation } = cartApi;
