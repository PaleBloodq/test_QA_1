export type OrderType = {
  date: string;
  amount: number;
  order_products: OrderCartType[];
  status: "PAID" | "OK" | "ERROR";
};

type OrderCartType = {
  item: string;
  description: string;
  price: number;
};
