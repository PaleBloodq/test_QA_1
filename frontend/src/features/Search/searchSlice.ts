import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SearchState {
  value: string;
  platforms: string[];
  languages: string[];
  lowPrice: number;
  highPrice: number;
  offset: number;
  limit: number;
}

const initialState: SearchState = {
  value: "",
  platforms: [],
  languages: [],
  lowPrice: 0,
  highPrice: 0,
  offset: 0,
  limit: 20,
};

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    setSearchValue: (state, action: PayloadAction<string>) => {
      state.value = action.payload;
    },
    setSearchPlatforms: (state, action: PayloadAction<string>) => {
      state.platforms = state.platforms.includes(action.payload)
        ? state.platforms.filter((item) => item !== action.payload)
        : [...state.platforms, action.payload];
    },
    setSearchLanguages: (state, action: PayloadAction<string>) => {
      state.languages = state.languages.includes(action.payload)
        ? state.languages.filter((item) => item !== action.payload)
        : [...state.languages, action.payload];
    },
    setSearchLowPrice: (state, action: PayloadAction<number>) => {
      state.lowPrice = action.payload;
    },
    setSearchHighPrice: (state, action: PayloadAction<number>) => {
      state.highPrice = action.payload;
    },
    setSearchOffset: (state, action: PayloadAction<number>) => {
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
