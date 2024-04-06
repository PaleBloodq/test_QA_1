import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  duration: 1,
  selectedSubscription: "",
};

const subscriptionSlice = createSlice({
  name: "subscriptionSlice",
  initialState,
  reducers: {
    setDuration: (state, action) => {
      state.duration = action.payload;
    },
    setSelectedSubscription: (state, action) => {
      state.selectedSubscription = action.payload;
    },
  },
});

export const { setDuration, setSelectedSubscription } = subscriptionSlice.actions;

export default subscriptionSlice.reducer;
