export type Publication = {
  id: string;
  title: string;
  original_price: number;
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
  preview: string;
  photo: string;
  discount_deadline: string;
};
