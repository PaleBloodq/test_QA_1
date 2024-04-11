import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  items: [],
  hasAccount: true,
  accountEmail: "",
  accountPassword: "",
  reciptEmail: "",
  rememberData: false,
  promocode: "",
};

const cartSlice = createSlice({
  name: "cartSlice",
  initialState,
  reducers: {
    addToCart: (state, action) => {
      if (!state.items.find((item) => item.id === action.payload.id)) {
        state.items = [...state.items, action.payload];
        console.log(state.items);
      }
    },
    deleteFromCart: (state, action) => {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
    setHasAccount: (state, action) => {
      state.hasAccount = action.payload;
    },
    setAccountEmail: (state, action) => {
      state.accountEmail = action.payload;
    },
    setAccountPassword: (state, action) => {
      state.accountPassword = action.payload;
    },
    setReciptEmail: (state, action) => {
      state.reciptEmail = action.payload;
    },
    setRememberData: (state, action) => {
      state.rememberData = action.payload;
    },
    setPromocode: (state, action) => {
      state.promocode = action.payload;
    },
  },
});

export const {
  addToCart,
  deleteFromCart,
  setAccountEmail,
  setAccountPassword,
  setHasAccount,
  setPromocode,
  setReciptEmail,
  setRememberData,
} = cartSlice.actions;

export default cartSlice.reducer;
