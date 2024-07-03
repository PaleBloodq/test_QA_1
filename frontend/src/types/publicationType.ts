export type PublicationType = {
  id: string;
  title: string;
  final_price: number;
  duration: number;
  quantity: number;
  includes: string;
  discount: number;
  cashback: number;
  is_main: boolean;
  languages: string[];
  ps_plus_discount: number;
  platforms: string[];
  product_page_image: string;
  search_image: string;
  offer_image: string;
  discount_deadline: string;
  product_type: "publication" | "add_on" | "subscription";
};
