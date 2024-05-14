import { CartItemType } from "../types/cartItem";

export default function calcTotalPrice(
  cartItems: CartItemType[],
  promoDiscount: number,
  cashbackUsed: number
) {
  let amount = cartItems.reduce((total, item) => total + item.final_price, 0);
  if (promoDiscount) {
    amount -= (amount * promoDiscount) / 100;
  }
  if (cashbackUsed >= amount) {
    return 0;
  } else {
    return amount - cashbackUsed;
  }
}
