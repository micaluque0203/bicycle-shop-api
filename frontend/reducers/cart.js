import { validateOrderItem } from "../services";

export const cartInitialState =
  JSON.parse(window.localStorage.getItem("cart")) || [];

export const CART_ACTION_TYPES = {
  ADD_TO_CART: "ADD_TO_CART",
  REMOVE_FROM_CART: "REMOVE_FROM_CART",
  CLEAR_CART: "CLEAR_CART",
};

export const updateLocalStorage = (state) => {
  window.localStorage.setItem("cart", JSON.stringify(state));
};

const UPDATE_STATE_BY_ACTION = {
  [CART_ACTION_TYPES.ADD_TO_CART]: (state, action) => {
    const { product_id, configuration, product } = action.payload;

    console.log("PRODUCT", product);

    const isValid = async () => {
      await validateOrderItem(product_id, configuration);
    };
    if (!isValid()) {
      throw new Error("Invalid configuration");
    }

    const productInCartIndex = state.findIndex(
      (item) =>
        item.product_id === product_id &&
        JSON.stringify(item.configuration) === JSON.stringify(configuration)
    );

    if (productInCartIndex >= 0) {
      const newState = [
        ...state.slice(0, productInCartIndex),
        {
          ...state[productInCartIndex],
          quantity: state[productInCartIndex].quantity + 1,
        },
        ...state.slice(productInCartIndex + 1),
      ];

      updateLocalStorage(newState);
      return newState;
    }

    const newState = [
      ...state,
      {
        ...action.payload,
        quantity: 1,
      },
    ];

    updateLocalStorage(newState);
    return newState;
  },
  [CART_ACTION_TYPES.REMOVE_FROM_CART]: (state, action) => {
    const { product_id, configuration } = action.payload;
    const newState = state.filter(
      (item) =>
        item.product_id !== product_id &&
        JSON.stringify(item.configuration) !== JSON.stringify(configuration)
    );
    updateLocalStorage(newState);
    return newState;
  },
  [CART_ACTION_TYPES.CLEAR_CART]: () => {
    updateLocalStorage([]);
    return [];
  },
};

export const cartReducer = (state, action) => {
  const { type: actionType } = action;
  const updateState = UPDATE_STATE_BY_ACTION[actionType];
  return updateState ? updateState(state, action) : state;
};
