import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const userApi = createApi({
  reducerPath: "userApi",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_DATABASE_URL,
    headers: {
      Authorization: `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6MTIzOTgxMjgzLCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA0LTI2VDIxOjI4OjQ1LjgxOTk0OSIsInRva2VuX3NlZWQiOiI5M2I5YjlhMjdkN2Q0OTU4YmEwZTM3MWJmNWFmNzA0MSJ9.ck82bCsxqMgXfxfHhR4Eoh3OWSrft0NgOmsnRYfFMXe7-ExbhcB-sFVRk0gnno--uUBYiE-mL-0ijorT0PpQa0KNOw9OJ0OJ-WWOg0B5Nc4WxdUpznjMUqNg8g2yP84VcGWic0wipt2h2CPg1To8GGll4rcLPGL4xhb9ULZ2bnnZODLLPOM4prxHTDA6VO-PzkYYok2DRMl46pnWYVZnUbha0B-v98YsnezXLZizM4WmIwrSGFRK1_xzOjPT2x2Fl5iMJep7HEOhKuiFvnhO-iod2B3aIiFjxvE_9zSUtUTOQmUiPXHq98XMCqjf9wWTXQqGGjhwbF7eURn82nUc-A`,
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
