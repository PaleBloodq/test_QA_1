import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_DATABASE_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI3VDExOjE2OjIzLjUxMTAyMyIsInRva2VuX3NlZWQiOiIwZmEzOTE0MTk1OWU0NGJkOGJiNGY2NzhjNDg5M2E5YyJ9.X3907e-8lOY29Oya2IMpAE0fm_RFd4MuMx420o8wPG52dcvedy9eXUK2GbRNd-iPNaaKTU95X8MswGHN0VTrnTwHVx2qOIMD1PBmtiP8AHUeUj0_T-Ku-hBP58NRK61wax1x20KkZt2QEXMf533wpkALoh9UDnBymDHKumZBoGkB9dy0NPRG0H5fZ9DP3wwZrFsCOBWIrVS0gTjNuvddT4BXmZtThV9cicpbSdbCRz4wKKZ9-0EQ7RVPp_HVi2QC48FbuaiF3yS8apn-SUSXph0fqg6Sehk15uuko61gqxIZLain1y8peqwHGN4oGCQ9SFuJEQsNUttQDNLXcqBghw`,
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
  }),
});

export const {
  useGetUserQuery,
  useGetOrdersQuery,
  useUpdateUserDataMutation,
  useMakeOrderMutation,
} = userApi;
