import { differenceInMonths, parseISO } from "date-fns";

export function isNew(date: string) {
  const releaseDate = parseISO(date);
  const isNew = differenceInMonths(new Date(), releaseDate) < 2;

  return isNew;
}
