import { useId } from "react";
import { useCart } from "../hooks/useCart.jsx";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/react";
import { ShoppingBagIcon } from "@heroicons/react/24/outline";
import CartItem from "./CartItem.jsx";

export function Cart() {
  const cartId = useId();
  const { cart } = useCart();
  const totalQuantity = cart.items.reduce(
    (total, item) => total + item.quantity,
    0
  );

  return (
    <>
      <Popover className="ml-4 flow-root text-sm lg:relative lg:ml-8">
        <PopoverButton
          className="group -m-2 flex items-center p-2"
          htmlFor={cartId}
        >
          <input id={cartId} type="checkbox" hidden />
          <ShoppingBagIcon
            aria-hidden="true"
            className="size-6 shrink-0 text-gray-400 group-hover:text-gray-500"
          />
          <span className="ml-2 text-sm font-medium text-gray-700 group-hover:text-gray-800">
            {totalQuantity}
          </span>
          <span className="sr-only">items in cart, view bag</span>
        </PopoverButton>
        <PopoverPanel
          transition
          className="absolute z-20 inset-x-0 top-16 mt-px bg-white pb-6 shadow-lg transition data-closed:opacity-0 data-enter:duration-200 data-enter:ease-out data-leave:duration-150 data-leave:ease-in sm:px-2 lg:top-full lg:right-0 lg:left-auto lg:mt-3 lg:-mr-1.5 lg:w-80 lg:rounded-lg lg:ring-1 lg:ring-black/5"
        >
          <h2 className="sr-only">Shopping Cart</h2>

          <form className="mx-auto max-w-2xl px-4">
            {cart.length === 0 && (
              <div className="min-h-16 flex items-center justify-center">
                <p className="py-1">No items in cart</p>
              </div>
            )}

            <ul role="list" className="divide-y divide-gray-200">
              {cart.items.map((product_cart) => {
                return (
                  <CartItem
                    key={product_cart.product_id}
                    id={product_cart.product_id}
                    name={product_cart.product.name}
                    category={product_cart.product.category}
                    quantity={product_cart.quantity}
                    configuration={product_cart.configuration}
                  />
                );
              })}
            </ul>
            {(cart.length === 0 && (
              <p className="mt-6 text-center">
                <a
                  href="/"
                  className="text-sm font-medium text-blue-600 hover:text-blue-500"
                >
                  Start Shopping Now
                </a>
              </p>
            )) || (
              <p className="mt-6 text-center">
                <a
                  href="/cart"
                  className="text-sm font-medium text-blue-600 hover:text-blue-500"
                >
                  View Shopping Bag
                </a>
              </p>
            )}
          </form>
        </PopoverPanel>
      </Popover>
    </>
  );
}

export default Cart;
