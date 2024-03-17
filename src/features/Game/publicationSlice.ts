import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  selectedPublication: "",
};

const publicationSlice = createSlice({
  name: "publicationSlice",
  initialState,
  reducers: {
    setSelectedPublication: (state, action) => {
      state.selectedPublication = action.payload;
    },
  },
});

export const { setSelectedPublication } = publicationSlice.actions;

export default publicationSlice.reducer;
