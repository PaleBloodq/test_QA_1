export type Addon = {
  id: string;
  product_type: "add_on";
  is_main: boolean;
  platforms: string[];
  final_price: number;
  discount: number;
  discount_deadline: null | string;
  ps_plus_final_price: null | number;
  ps_plus_discount: number;
  ps_plus_discount_deadline: null | string;
  languages: string[];
  title: string;
  includes: null | string;
  product_page_image: string;
  search_image: string;
  offer_image: string;
  cashback: number;
  type: string;
};
