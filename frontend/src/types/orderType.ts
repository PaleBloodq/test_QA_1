export type OrderType = {
  date: string;
  totalCost: number;
  cart: OrderCartType[];
};

type OrderCartType = {
  name: string;
  description: string;
  price: number;
};
