export type OrderType = {
  date: string;
  amount: number;
  order_products: OrderCartType[];
};

type OrderCartType = {
  item: string;
  description: string;
  price: number;
};
