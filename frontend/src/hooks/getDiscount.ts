export function getDiscount(number: number, discount: number): number {
  return Number((Math.round((number - (number * discount) / 100) * 100) / 100).toFixed(0));
}
