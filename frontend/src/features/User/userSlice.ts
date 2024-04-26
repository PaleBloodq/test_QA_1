import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  userData: {
    playstation_email: "",
    playstation_password: "",
    bill_email: "",
    cashback: 0,
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
