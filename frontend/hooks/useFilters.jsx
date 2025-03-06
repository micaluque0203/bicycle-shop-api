import { FiltersContext } from "../context/filters";
import { useContext } from "react";

export function useFilters() {
  const { filters, setFilters } = useContext(FiltersContext);

  console.log(filters);
  const filterProducts = (products) => {
    return products.filter((product) => {
      return (
        product.price <= filters.maxPrice &&
        (filters.category === "all" || product.category === filters.category)
      );
    });
  };
  return { filters, filterProducts, setFilters };
}
