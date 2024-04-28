import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  username: "",
  isLoggined: false,
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
    setIsLoggined: (state, action) => {
      state.isLoggined = action.payload;
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
  setIsLoggined,
} = userSlice.actions;

export default userSlice.reducer;
