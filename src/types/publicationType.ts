import { Discount } from "./gameType";

export type Publication = {
  id: string;
  title: string;
  price: Price[];
  includes: string[];
  discount: Discount;
  cashback: number;
  psPlusDiscount?: number;
};

export type Price = {
  platform: string;
  price: number;
};

export type Publications = Publication[];
