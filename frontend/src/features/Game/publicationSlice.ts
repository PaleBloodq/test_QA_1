import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  selectedPublication: "",
  selectedPlatform: "",
};

const publicationSlice = createSlice({
  name: "publicationSlice",
  initialState,
  reducers: {
    setSelectedPublication: (state, action) => {
      state.selectedPublication = action.payload;
    },
    setSelectedPlatform: (state, action) => {
      state.selectedPlatform = action.payload;
    },
  },
});

export const { setSelectedPublication, setSelectedPlatform } = publicationSlice.actions;

export default publicationSlice.reducer;
