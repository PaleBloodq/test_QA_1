export type OrderType = {
  date: string;
  amount: number;
  order_products: OrderItemType[];
  status: "PAID" | "ERROR" | "OK" | "PAYMENT" | "IN_PROGRESS" | "COMPLETED";
  payment_url: string;
};

type OrderItemType = {
  item: string;
  description: string;
  final_price: number;
};
