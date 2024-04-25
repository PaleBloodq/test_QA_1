import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_DATABASE_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI1VDIyOjUwOjAwLjk3NDM4NyIsInRva2VuX3NlZWQiOiJkMWU0ODVhZmYyOTA0ZDFlYTgxYTIxNzc1MzZlZTA3MSJ9.tr_ObG4cwLG_2UF0i31Hikz4hBTxAJ7GlzE5AoyCFbORaV0FrBz3-_Dj6i2ZGTxv80JsPa2Z9umVsSNMbNyAPvK2-hUcpk7ItyqDhrwD7mMojHHsIopZ-H_jXgSzjRxjY2zkn7yjFaj6GUs6wQrn8XMvQPRxVyZt28mivuZfhW1OCKXP1SNw7kc94LeRVR7qXSAqXfggf0KaMeeadp2KQCy8Z6LgQYZ4GxagN02zQ-RQztr305vPgGVJ3SsdcozA1N3cncSlGSerOZ4zDrBlTSp9XDb4iBUEfUtWCNAvMGSzkGfIJoK6ocnaLScdBE6sNqwF_mL-3c6JsSq3GGSt3w`,
    },
  }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: () => `profile/`,
    }),
    getOrders: builder.query({
      query: () => `orders/`,
    }),
    updateUserData: builder.mutation({
      query: ({ updatedData }) => ({
        url: `profile/update`,
        method: "POST",
        body: updatedData,
      }),
    }),
  }),
});

export const { useGetUserQuery, useGetOrdersQuery, useUpdateUserDataMutation } = userApi;
