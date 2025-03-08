import { useReducer, createContext } from "react";
import { cartReducer, cartInitialState } from "../reducers/cart.js";
import { validateOrderItem } from "../services";

export const CartContext = createContext();

function useCartReducer() {
  const [state, dispatch] = useReducer(cartReducer, cartInitialState);

  const addToCart = async (product_id, configuration, product) => {
    console.log("addToCart", product);
    try {
      const response = await validateOrderItem({
        product_id: product_id,
        configuration: configuration,
      });
      if (!response.is_valid) {
        dispatch({
          type: "ADD_TO_CART_FAILURE",
          payload: "Invalid configuration",
        });
        return;
      }
      dispatch({
        type: "ADD_TO_CART_SUCCESS",
        payload: { product_id, configuration, product },
      });
    } catch (error) {
      dispatch({
        type: "ADD_TO_CART_FAILURE",
        payload: "Invalid configuration",
      });
    }
  };

  const removeFromCart = (product) =>
    dispatch({
      type: "REMOVE_FROM_CART",
      payload: product,
    });

  const clearCart = () => dispatch({ type: "CLEAR_CART" });

  return { state, addToCart, removeFromCart, clearCart };
}

export function CartProvider({ children }) {
  const { state, addToCart, removeFromCart, clearCart } = useCartReducer();

  return (
    <CartContext.Provider
      value={{
        cart: state,
        addToCart,
        removeFromCart,
        clearCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}
