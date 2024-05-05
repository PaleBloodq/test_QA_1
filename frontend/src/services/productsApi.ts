import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { ProductType } from "../types/ProductType";
import { Publication } from "../types/PublicationType";

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
    getAnyPublication: builder.query<Publication, string>({
      query: (id) => `api/publication/${id}`,
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
  useGetAnyPublicationQuery,
} = productsApi;
