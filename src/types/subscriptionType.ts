export type subscriptionType = {
  id: string;
  type: string;
  title: string;
  platforms: string[];
  languages: string[];
  photoUrls: string[];
  previewImg: string;
  releaseDate: string;
  durationVariations: durationVariationsType[];
};

export type durationVariationsType = {
  id: string;
  title: string;
  price: SubscriptionPriceType[];
  photoUrls: string[];
  previewImg: string;
  discriptin: string;
  includes: string[];
  discount: {
    percent: number;
    deadline: string;
  };
  cashback: number;
};

export type SubscriptionPriceType = {
  duration: number;
  price: number;
};
