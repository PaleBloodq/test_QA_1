import { PublicationType } from "../types/publicationType";

export function findCheapestPublication(publications: PublicationType[]) {
  const sortedPublications = [...publications].sort((a, b) => a.final_price - b.final_price);
  return sortedPublications[0];
}
