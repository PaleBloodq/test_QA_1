import { createSlice } from "@reduxjs/toolkit";
import { act } from "react-dom/test-utils";

const initialState = {
  username: "",
  userData: {
    playstation_email: "",
    playstation_password: "",
    bill_email: "",
    cashback: 0,
  },
  updatedData: {
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
      state.updatedData = action.payload;
    },
    updateAccountMail: (state, action) => {
      state.updatedData.psEmail = action.payload;
    },
    updateAccountPassword: (state, action) => {
      state.updatedData.psPassword = action.payload;
    },
    updateBillMail: (state, action) => {
      state.updatedData.billEmail = action.payload;
    },
    setUserName: (state, action) => {
      state.username = action.payload;
    },
  },
});

export const {
  setUserData,
  updateAccountMail,
  updateAccountPassword,
  updateBillMail,
  setUpdateData,
  setUserName,
} = userSlice.actions;

export default userSlice.reducer;
