export type Publication = {
  id: string;
  title: string;
  price: Price[];
  includes?: string[];
};

export type Price = {
  platform: string;
  price: number;
};

export type Publications = Publication[];
