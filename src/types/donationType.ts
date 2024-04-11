export type donationType = {
  id: string;
  type: string;
  title: string;
  photoUrls: string[];
  previewImg: string;
  platforms: string[];
  languages: string[];
  releaseDate: string;
  quantityVariations: QuantityVariations[];
  unitPrice: number;
};

export type QuantityVariations = {
  id: string;
  count: number;
};
