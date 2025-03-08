export const cartInitialState = JSON.parse(
  window.localStorage.getItem("cart")
) || {
  items: [],
  error: null,
};

export const CART_ACTION_TYPES = {
  ADD_TO_CART: "ADD_TO_CART",
  ADD_TO_CART_SUCCESS: "ADD_TO_CART_SUCCESS",
  ADD_TO_CART_FAILURE: "ADD_TO_CART_FAILURE",
  ADD_TO_CART_OUT_OF_STOCK: "ADD_TO_CART_OUT_OF_STOCK",
  REMOVE_FROM_CART: "REMOVE_FROM_CART",
  CLEAR_CART: "CLEAR_CART",
};

export const updateLocalStorage = (state) => {
  window.localStorage.setItem("cart", JSON.stringify(state));
};

const UPDATE_STATE_BY_ACTION = {
  [CART_ACTION_TYPES.ADD_TO_CART_SUCCESS]: (state, action) => {
    const { product_id, configuration, product } = action.payload;

    const productInCartIndex = state.items.findIndex(
      (item) =>
        item.product_id === product_id &&
        JSON.stringify(item.configuration) === JSON.stringify(configuration)
    );

    if (productInCartIndex >= 0) {
      return {
        ...state,
        items: [
          ...state.items.slice(0, productInCartIndex),
          {
            ...state.items[productInCartIndex],
            quantity: state.items[productInCartIndex].quantity + 1,
          },
          ...state.items.slice(productInCartIndex + 1),
        ],
        error: null,
      };
    }

    const newState = {
      ...state,
      items: [
        ...state.items,
        {
          product_id,
          configuration,
          product,
          quantity: 1,
        },
      ],
      error: null,
    };
    console.log(newState);
    updateLocalStorage(newState);
    return newState;
  },

  [CART_ACTION_TYPES.REMOVE_FROM_CART]: (state, action) => {
    const { product_id, configuration } = action.payload;
    const newStateItems = state.items.filter(
      (item) =>
        item.product_id !== product_id &&
        JSON.stringify(item.configuration) !== JSON.stringify(configuration)
    );
    updateLocalStorage({ items: newStateItems, error: null });
    return { items: newStateItems, error: null };
  },
  [CART_ACTION_TYPES.ADD_TO_CART_FAILURE]: (state, action) => {
    return {
      ...state,
      error: action.payload,
    };
  },
  [CART_ACTION_TYPES.CLEAR_CART]: () => {
    updateLocalStorage({ items: [], error: null });
    return { items: [], error: null };
  },
};

export const cartReducer = (state, action) => {
  const { type: actionType } = action;
  const updateState = UPDATE_STATE_BY_ACTION[actionType];
  return updateState ? updateState(state, action) : state;
};
