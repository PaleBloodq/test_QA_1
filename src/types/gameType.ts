export type gameType = {
  id: string;
  type: string;
  title: string;
  photoUrls: string[];
  previewImg: string;
  platforms: string[];
  languages: string[];
  releaseDate: string;
  publications: Publication[];
  discount?: Discount;
  psPlusDiscount?: number;
  cashback?: number;
};

type Publication = {
  id: string;
  title: string;
  price: Price;
  includes?: string[]; // Опциональное поле, поскольку не все публикации его имеют
};

type Discount = {
  percent: number;
  deadline: string;
};

type Price = {
  platform: string;
  price: number;
};
