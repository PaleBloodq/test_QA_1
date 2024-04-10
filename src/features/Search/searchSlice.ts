import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

const searchSlice = createSlice({
  name: "search",
  initialState: {
    value: "",
    platforms: [],
    languages: [],
    lowPrice: 0,
    highPrice: 0,
    offset: 0,
    limit: 20,
  },
  reducers: {
    setSearchValue: (state, action: PayloadAction<string>) => {
      state.value = action.payload;
    },
    setSearchPlatforms: (state, action) => {
      state.platforms = state.platforms.includes(action.payload)
        ? state.platforms.filter((item) => item !== action.payload)
        : [...state.platforms, action.payload];
    },
    setSearchLanguages: (state, action) => {
      state.languages = state.languages.includes(action.payload)
        ? state.languages.filter((item) => item !== action.payload)
        : [...state.languages, action.payload];
    },
    setSearchLowPrice: (state, action) => {
      state.lowPrice = action.payload;
    },
    setSearchHighPrice: (state, action) => {
      state.highPrice = action.payload;
    },
    setSearchOffset: (state, action) => {
      state.offset = action.payload;
    },
  },
});

export const {
  setSearchValue,
  setSearchPlatforms,
  setSearchLanguages,
  setSearchLowPrice,
  setSearchHighPrice,
  setSearchOffset,
} = searchSlice.actions;
export default searchSlice.reducer;
