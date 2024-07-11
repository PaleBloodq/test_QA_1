import { useState, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { searchSelector } from "../features/Search/searchSelectors";
import { useGetSearchProductsMutation } from "../services/productsApi";
import { setSearchValue } from "../features/Search/searchSlice";

const useMultiTypeSearch = (typenames: string[]) => {
  const dispatch = useDispatch();
  const { value, languages, limit, maxPrice, minPrice, offset, platforms } =
    useSelector(searchSelector);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const [getSearchProducts] = useGetSearchProductsMutation();

  const fetchProducts = useCallback(
    async (typenameIndex = 0, accumulatedProducts = []) => {
      if (typenameIndex >= typenames.length) {
        setProducts(accumulatedProducts);
        setIsLoading(false);
        return;
      }

      const params = {
        minPrice,
        maxPrice,
        platforms,
        languages,
        typename: typenames[typenameIndex],
        limit,
        q: value,
        offset,
      };

      setIsLoading(true);

      try {
        const result = await getSearchProducts({ params }).unwrap();
        const newProducts = [...accumulatedProducts, ...result];

        if (newProducts.length < 20 && typenameIndex < typenames.length - 1) {
          fetchProducts(typenameIndex + 1, newProducts);
        } else {
          setProducts(newProducts);
          setIsLoading(false);
        }
      } catch (error) {
        setIsLoading(false);
        console.error("Error fetching products:", error);
      }
    },
    [value, languages, maxPrice, minPrice, offset, platforms, limit, typenames, getSearchProducts]
  );

  const handleSearch = () => {
    fetchProducts(0, []);
  };

  return {
    products,
    isLoading,
    handleSearch,
    setSearchValue: (value: string) => dispatch(setSearchValue(value)),
  };
};

export default useMultiTypeSearch;
