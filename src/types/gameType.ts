import { Publication } from "./publicationType";

export type gameType = {
  id: string;
  type: string;
  title: string;
  photoUrls: string[];
  previewImg: string;
  platforms: string[];
  languages: string[];
  releaseDate: string;
  publications: Publication[];
};

export type Discount = {
  percent: number;
  deadline: string;
};
