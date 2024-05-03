export default function calcCashback(price: number, cashback: number): number {
  return Math.round((cashback / 100) * price);
}
