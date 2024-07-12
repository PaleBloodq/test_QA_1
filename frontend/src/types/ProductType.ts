import { AddonType } from "./AddonType";
import { PublicationType } from "./publicationType";

export type ProductType = {
  id: string;
  type: "GAME" | "SUBSCRIPTION" | "DONATION";
  title: string;
  release_date: string;
  publications: PublicationType[];
  add_ons: AddonType[];
};
