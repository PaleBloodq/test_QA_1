import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_DATABASE_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI2VDEyOjU2OjA5LjIyNDA0NyIsInRva2VuX3NlZWQiOiI2ZTM2YWM3MTQyNGY0YTE4ODRjNGUwMmZiYWQyODU4YSJ9.Y0UpTSPov4CaZfBILiTY4quR4rzCwxMZZcp0Y8qAZ4WoUweO7B3TclREaHNQhCNcAo5cglozVPDvjAv0W6moqz9KWrPOnG0b7nyiQM3S__unu_TS2Hz11YrDUQ1mNNotCWKHdujWDUbO0wFWPuKHyVF-tjN7Rwrui8_I9HKI6ubiXINID-9sdU-u6nEc0IAp3uz5JI5Y8t5HtlMNlsrtp46dbL2wE07n2NlEnNKGmR0khZHb_Kk-Dy_XMuUe1adP-CaFGwdvBFL28iczS7_8cJbCRDdPasBsKGmaLe3fZIf06KG-0fxkCgMm4iXwoJW3HUriUtDcHrFGSUY-p08cLw`,
    },
  }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: () => `profile/`,
    }),
    getOrders: builder.query({
      query: () => `profile/orders/?limit=10&offset=0`,
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
