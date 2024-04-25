export type FilterInitData = {
  platforms: Objects[];
  languages: Objects[];
  minPrice: number;
  maxPrice: number;
};

type Objects = {
  id: string;
  name: string;
};
