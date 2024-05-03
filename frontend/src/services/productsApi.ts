import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ProductType } from "../types/ProductType";

export const productsApi = createApi({
  reducerPath: "productsApi",
  baseQuery: fetchBaseQuery({ baseUrl: import.meta.env.VITE_API_URL }),
  endpoints: (builder) => ({
    getCategoryProducts: builder.query({
      query: () => `api/catalog/category/`,
    }),
    getAnyProduct: builder.query<ProductType, string>({
      query: (id) => `api/product/${id}`,
    }),
    getSearchProducts: builder.mutation({
      query: ({ params }) => ({
        url: `api/catalog/search/list/`,
        method: "POST",
        body: params,
      }),
    }),
    getSearchFilters: builder.query({
      query: () => `api/catalog/filters/`,
    }),
  }),
});

export const {
  useGetCategoryProductsQuery,
  useGetAnyProductQuery,
  useGetSearchProductsMutation,
  useGetSearchFiltersQuery,
} = productsApi;
