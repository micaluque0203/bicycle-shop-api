import React, { useEffect, useState } from "react";
import ProductsList from "../components/ProductsList.jsx";
import { useAdmin } from "../hooks/useAdmin.jsx";

export function Home() {
  const { admin_dash, fetchProducts } = useAdmin();

  useEffect(() => {
    async function fetchData() {
      if (admin_dash.products.length === 0) {
        await fetchProducts();
      }
    }
    fetchData();
  }, [admin_dash.products]);

  return <ProductsList products={admin_dash.products}></ProductsList>;
}
