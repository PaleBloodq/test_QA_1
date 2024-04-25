import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ProductType } from "../types/ProductType";

export const productsApi = createApi({
  reducerPath: "productsApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_DATABASE_URL }),
  endpoints: (builder) => ({
    getCategoryProducts: builder.query({
      query: () => `/catalog/category/?format=json`,
    }),
    getAnyProduct: builder.query<ProductType, string>({
      query: (id) => `/product/${id}`,
    }),
    getSearchProducts: builder.query({
      query: () => `/searchItems/`,
    }),
    getSearchFilters: builder.query({
      query: () => `/filters`,
    }),
  }),
});

export const {
  useGetCategoryProductsQuery,
  useGetAnyProductQuery,
  useGetSearchProductsQuery,
  useGetSearchFiltersQuery,
} = productsApi;
