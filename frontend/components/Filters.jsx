import { useId } from "react";
import { useFilters } from "../hooks/useFilters.jsx";
import "./Filters.css";

export function Filters() {
  const { filters, setFilters } = useFilters();

  const minPriceFilterId = useId();
  const categoryFilterId = useId();

  const handleChangeMinPrice = (event) => {
    setFilters((prevState) => ({
      ...prevState,
      maxPrice: event.target.value,
    }));
  };

  const handleChangeCategory = (event) => {
    // TODO: change the category in the filters state
    setFilters((prevState) => ({
      ...prevState,
      category: event.target.value,
    }));
  };

  return (
    <section className="filters">
      <div>
        <label htmlFor={minPriceFilterId}>Max price:</label>
        <input
          type="range"
          id={minPriceFilterId}
          min="0"
          max="1000"
          onChange={handleChangeMinPrice}
          value={filters.maxPrice}
        />
        <span>${filters.maxPrice}</span>
      </div>
      <div>
        <label htmlFor={categoryFilterId}>Category</label>
        <select id={categoryFilterId} onChange={handleChangeCategory}>
          <option value="all">All</option>
          <option value="laptops">Beauty</option>
          <option value="smartphones">Celulares</option>
        </select>
      </div>
    </section>
  );
}
