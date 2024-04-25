import { Publication } from "./PublicationType";

export type ProductType = {
  id: string;
  type: "GAME" | "SUBSCRIPTION" | "DONATION";
  title: string;
  languages: string[];
  release_date: string;
  publications: Publication[];
};
