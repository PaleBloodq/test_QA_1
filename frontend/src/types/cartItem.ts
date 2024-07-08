export type CartItemType = {
  id: string;
  type: string;
  img: string;
  title: string;
  publication: string;
  platform: string;
  price: number;
  final_price: number;
  discount: number;
  cashback: number;
  product_type: "add_on" | "publication" | "subscription";
};
