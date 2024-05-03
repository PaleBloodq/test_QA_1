import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ProductType } from "../types/ProductType";

export const productsApi = createApi({
  reducerPath: "productsApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_API_URL }),
  endpoints: (builder) => ({
    getCategoryProducts: builder.query({
      query: () => `/catalog/category/`,
    }),
    getAnyProduct: builder.query<ProductType, string>({
      query: (id) => `/product/${id}`,
    }),
    getSearchProducts: builder.mutation({
      query: ({ params }) => ({
        url: `/catalog/search/list/`,
        method: "POST",
        body: params,
      }),
    }),
    getSearchFilters: builder.query({
      query: () => `/catalog/filters/`,
    }),
  }),
});

export const {
  useGetCategoryProductsQuery,
  useGetAnyProductQuery,
  useGetSearchProductsMutation,
  useGetSearchFiltersQuery,
} = productsApi;
