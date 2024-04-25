import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: 0,
};

const currentPriceSlice = createSlice({
  name: "currentPriceSlice",
  initialState,
  reducers: {
    setCurrentPrice: (state, action) => {
      state.value = action.payload;
    },
  },
});

export const { setCurrentPrice } = currentPriceSlice.actions;

export default currentPriceSlice.reducer;
