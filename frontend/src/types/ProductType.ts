import { Addon } from "./Addon";
import { PublicationType } from "./PublicationType";

export type ProductType = {
  id: string;
  type: "GAME" | "SUBSCRIPTION" | "DONATION";
  title: string;
  release_date: string;
  publications: PublicationType[];
  add_ons: Addon[];
};
