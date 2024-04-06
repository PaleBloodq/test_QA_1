import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const productsApi = createApi({
  reducerPath: "productsApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_DATABASE_URL }),
  endpoints: (builder) => ({
    getCategoryProducts: builder.query({
      query: () => `/category`,
    }),
    getAnyProduct: builder.query({
      query: (id) => `/any/${id}`,
    }),
  }),
});

export const { useGetCategoryProductsQuery, useGetAnyProductQuery } = productsApi;
