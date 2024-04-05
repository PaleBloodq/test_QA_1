import { useEffect, useState } from "react";

export default function useIsLoading(data: unknown) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (data) {
      setIsLoading(false);
    }
  }, [data]);

  return isLoading;
}
