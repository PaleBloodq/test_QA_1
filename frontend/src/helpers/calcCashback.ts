export default function calcCashback(price: number, cashback: number): number {
  return (cashback / 100) * price;
}
