export type subscriptionType = {
  id: string;
  type: string;
  title: string;
  photoUrls: string[];
  previewImg: string;
  platforms: string[];
  languages: string[];
  releaseDate: string;
  durationVariations: [{ duration: number; price: number }];
  discount: {
    percent: number;
    deadline: string;
  };
  psPlusDiscount: number;
  cashback: number;
};
