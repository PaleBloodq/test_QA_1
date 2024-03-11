export type Game = {
  id: string;
  name: string;
  img: string;
  platform: string;
  language: string;
  releaseDate: string;
  publications: Publication[];
  discount?: Discount;
  psPlusDiscount?: string;
  cashback?: string;
  tags?: string[];
};

type Publication = {
  title: string;
  price: string;
  includes?: string[]; // Опциональное поле, поскольку не все публикации его имеют
};

type Discount = {
  active: boolean;
  percent: string;
  deadline: string;
};
