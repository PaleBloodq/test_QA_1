import { Discount } from "./gameType";

export type Publication = {
  id: string;
  title: string;
  price: PriceType[];
  includes: string[];
  discount: Discount;
  cashback: number;
  psPlusDiscount: number;
};

export type PriceType = {
  platform: string;
  price: number;
};

export type Publications = Publication[];
