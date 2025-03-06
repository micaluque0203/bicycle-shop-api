import React from "react";
import RelatedProducts from "../components/RelatedProducts.jsx";
import CartContainer from "../components/CartContainer.jsx";

export function CartPage() {
  return (
    <main className="m-16">
      <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
        Shopping Cart
      </h1>

      <div className="mx-2">
        <CartContainer />
        <RelatedProducts />
      </div>
    </main>
  );
}
