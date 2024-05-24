import { CartItemType } from "../types/cartItem";

export default function calcOrderCashback(
  cartItems: CartItemType[],
  promoCodeDiscount: number
): number {
  let totalCashback = 0;
  cartItems.forEach((item) => (totalCashback += (item.final_price * item.cashback) / 100));
  if (promoCodeDiscount) {
    totalCashback = totalCashback - (totalCashback * promoCodeDiscount) / 100;
  }
  return totalCashback;
}
