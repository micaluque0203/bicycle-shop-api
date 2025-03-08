import React from "react";
import { useCart } from "../hooks/useCart.jsx";
import { useId } from "react";
import {
  QuestionMarkCircleIcon,
  XMarkIcon as XMarkIconMini,
} from "@heroicons/react/20/solid";
const CartContainer = () => {
  const { cart, removeFromCart } = useCart();

  return (
    <>
      {(cart.items.length > 0 && (
        <form className="mt-12 lg:grid lg:grid-cols-12 lg:items-start lg:gap-x-12 xl:gap-x-16">
          <section aria-labelledby="cart-heading" className="lg:col-span-7">
            <h2 id="cart-heading" className="sr-only">
              Items in your shopping cart
            </h2>
            <ul
              role="list"
              className="divide-y divide-gray-200 border-t border-b border-gray-200"
            >
              {cart.items.map((product_cart) => {
                const id = useId();
                return (
                  <li key={id} className="flex py-6 sm:py-10">
                    <div className="shrink-0">
                      <img
                        alt={product_cart.product.name}
                        src="/assets/josh-nuttall-zkVi57UYHIQ-unsplash.jpg"
                        className="size-24 rounded-md object-cover sm:size-48"
                      />
                    </div>
                    <div className="ml-4 flex flex-1 flex-col justify-between sm:ml-6">
                      <div className="relative pr-9 sm:grid sm:grid-cols-2 sm:gap-x-6 sm:pr-0">
                        <div>
                          <div className="flex justify-between">
                            <h3 className="text-sm">
                              <a
                                href={`/products/${product_cart.product.product_id}`}
                                className="font-medium text-gray-700 hover:text-gray-800"
                              >
                                {product_cart.product.name}
                              </a>
                            </h3>
                          </div>
                          <p className="mt-1 text-sm text-gray-700">
                            {product_cart.product.category} - Quantity{" "}
                            {product_cart.quantity}
                          </p>
                          <div>
                            <ul className="text-gray-500 text-sm mt-1">
                              {product_cart.configuration.map((item, index) => {
                                const key = Object.keys(item)[0];
                                const value = item[key];
                                return (
                                  <li key={index}>
                                    {" "}
                                    {key} | {value}{" "}
                                  </li>
                                );
                              })}
                            </ul>
                          </div>
                          <div className="absolute top-0 right-0">
                            <button
                              type="button"
                              onClick={() =>
                                removeFromCart(product_cart.product)
                              }
                              className="-m-2 inline-flex p-2 text-gray-400 hover:text-gray-500"
                            >
                              <span className="sr-only">Remove</span>
                              <XMarkIconMini
                                aria-hidden="true"
                                className="size-5"
                              />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </section>

          {/* Order summary Mock*/}
          <section
            aria-labelledby="summary-heading"
            className="mt-16 rounded-lg bg-gray-50 px-4 py-6 sm:p-6 lg:col-span-5 lg:mt-0 lg:p-8"
          >
            <h2
              id="summary-heading"
              className="text-lg font-medium text-gray-900"
            >
              Order summary mocked
            </h2>

            <dl className="mt-6 space-y-4">
              <div className="flex items-center justify-between">
                <dt className="text-sm text-gray-600">Subtotal</dt>
                <dd className="text-sm font-medium text-gray-900">$99.00</dd>
              </div>
              <div className="flex items-center justify-between border-t border-gray-200 pt-4">
                <dt className="flex items-center text-sm text-gray-600">
                  <span>Shipping estimate</span>
                  <a
                    href="#"
                    className="ml-2 shrink-0 text-gray-400 hover:text-gray-500"
                  >
                    <span className="sr-only">
                      Learn more about how shipping is calculated
                    </span>
                    <QuestionMarkCircleIcon
                      aria-hidden="true"
                      className="size-5"
                    />
                  </a>
                </dt>
                <dd className="text-sm font-medium text-gray-900">$5.00</dd>
              </div>
              <div className="flex items-center justify-between border-t border-gray-200 pt-4">
                <dt className="flex text-sm text-gray-600">
                  <span>Tax estimate</span>
                  <a
                    href="#"
                    className="ml-2 shrink-0 text-gray-400 hover:text-gray-500"
                  >
                    <span className="sr-only">
                      Learn more about how tax is calculated
                    </span>
                    <QuestionMarkCircleIcon
                      aria-hidden="true"
                      className="size-5"
                    />
                  </a>
                </dt>
                <dd className="text-sm font-medium text-gray-900">$8.32</dd>
              </div>
              <div className="flex items-center justify-between border-t border-gray-200 pt-4">
                <dt className="text-base font-medium text-gray-900">
                  Order total
                </dt>
                <dd className="text-base font-medium text-gray-900">$112.32</dd>
              </div>
            </dl>

            <div className="mt-6">
              <button
                type="submit"
                className="w-full rounded-md border border-transparent bg-blue-600 px-4 py-3 text-base font-medium text-white shadow-xs hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-50 focus:outline-hidden"
              >
                Checkout
              </button>
            </div>
          </section>
        </form>
      )) || (
        <div className="mt-6 text-sm w-full">
          <div>
            <p className="text-sm">No products in your cart.</p>
          </div>
          <div>
            <a
              href="/"
              className="block font-medium text-indigo-600 hover:text-indigo-500 mt-4"
            >
              Start Shopping
              <span aria-hidden="true"> &rarr;</span>
            </a>
          </div>
        </div>
      )}
    </>
  );
};

export default CartContainer;
