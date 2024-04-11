import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  userData: {
    accountEmail: "mazafaka@gmail.com",
    accountPassword: "zxcqwe",
    billEmai: "papafaka@mail.ru",
    cashback: 50,
  },
};

const userSlice = createSlice({
  name: "userSlice",
  initialState,
  reducers: {
    setUserData: (state, action) => {
      state.userData = action.payload;
    },
  },
});

export const { setUserData } = userSlice.actions;

export default userSlice.reducer;
