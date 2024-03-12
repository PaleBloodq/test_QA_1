type SubscriptionPrice = {
  period: string;
  value: string;
};

export type SubscriptionType = {
  name: string;
  price: SubscriptionPrice[];
  description: string;
  platform: string;
  previewImg: string;
};
