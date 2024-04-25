export type SearchItemType = {
  id: string;
  title: string;
  pubTitle: string;
  type: string;
  previewImg: string;
  prices: Array<{ platform: string; price: number }>;
  photoUrls: string[];
  includes: string[];
  discount?: {
    percent: number;
    deadline: string;
  };
  psPlusDiscount?: number;
  cashback?: number;
  description?: string;
};
