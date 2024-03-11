import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const productsApi = createApi({
  reducerPath: "productsApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:3000/" }),
  endpoints: (builder) => ({
    getProducts: builder.query({
      query: () => `games`,
    }),
    getProduct: builder.query({
      query: (id) => `games/${id}`,
    }),
  }),
});

export const { useGetProductsQuery } = productsApi;
