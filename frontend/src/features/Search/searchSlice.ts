import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SearchState {
  value: string;
  platforms: string[];
  languages: string[];
  minPrice: number;
  maxPrice: number;
  offset: number;
  limit: number;
}

const initialState: SearchState = {
  value: "",
  platforms: [],
  languages: [],
  minPrice: 0,
  maxPrice: 0,
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
      state.minPrice = action.payload;
    },
    setSearchHighPrice: (state, action: PayloadAction<number>) => {
      state.maxPrice = action.payload;
    },
    setSearchOffset: (state, action: PayloadAction<number>) => {
      state.offset = action.payload;
    },
    resetSearchSettings: (state, action) => {
      state.value = "";
      state.languages = [];
      state.platforms = [];
      state.minPrice = action.payload.minPrice;
      state.maxPrice = action.payload.maxPrice;
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
  resetSearchSettings,
} = searchSlice.actions;

export default searchSlice.reducer;
