import { createSlice } from "@reduxjs/toolkit";
import { CartItemType } from "../../types/cartItem";

type State = {
  items: CartItemType[];
  hasAccount: boolean;
  accountEmail: string;
  accountPassword: string;
  reciptEmail: string;
  rememberData: boolean;
  promocode: string;
  totalPrice: number;
  totalCashback: number;
};

const initialState: State = {
  items: [],
  hasAccount: true,
  accountEmail: "",
  accountPassword: "",
  reciptEmail: "",
  rememberData: false,
  promocode: "",
  totalPrice: 0,
  totalCashback: 0,
};

const cartSlice = createSlice({
  name: "cartSlice",
  initialState,
  reducers: {
    addToCart: (state, action) => {
      if (!state.items.find((item) => item.id === action.payload.id)) {
        state.items = [...state.items, action.payload];
      }
    },
    deleteFromCart: (state, action) => {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
    clearCart: (state) => {
      state.items = [];
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
    setTotalPrice: (state, action) => {
      state.totalPrice = action.payload;
    },
    setTotalCashback: (state, action) => {
      state.totalCashback = action.payload;
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
  clearCart,
  setTotalPrice,
  setTotalCashback,
} = cartSlice.actions;

export default cartSlice.reducer;
