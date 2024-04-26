import { createSlice } from "@reduxjs/toolkit";
import { act } from "react-dom/test-utils";

const initialState = {
  userData: {
    playstation_email: "",
    playstation_password: "",
    bill_email: "",
    cashback: 0,
  },
  updateData: {
    psEmail: "",
    psPassword: "",
    billEmail: "",
  },
};

const userSlice = createSlice({
  name: "userSlice",
  initialState,
  reducers: {
    setUserData: (state, action) => {
      state.userData = action.payload;
    },
    setUpdateData: (state, action) => {
      state.updateData = action.payload;
    },
    updateAccountMail: (state, action) => {
      state.updateData.psEmail = action.payload;
    },
    updateAccountPassword: (state, action) => {
      state.updateData.psPassword = action.payload;
    },
    updateBillMail: (state, action) => {
      state.updateData.billEmail = action.payload;
    },
  },
});

export const {
  setUserData,
  updateAccountMail,
  updateAccountPassword,
  updateBillMail,
  setUpdateData,
} = userSlice.actions;

export default userSlice.reducer;
