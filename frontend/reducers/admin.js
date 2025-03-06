export const ADMIN_ACTION_TYPES = {
  SET_PRODUCTS: "SET_PRODUCTS",
  SET_PARTS: "SET_PARTS",
  SET_RULE: "SET_RULE",
  ADD_PRODUCT: "ADD_PRODUCT",
  ADD_PART: "ADD_PART",
  ADD_RULE: "ADD_RULE",
};

const UPDATE_STATE_BY_ACTION = {
  [ADMIN_ACTION_TYPES.SET_PRODUCTS]: (state, action) => {
    const newState = { ...state, products: action.payload };
    window.localStorage.setItem("admin", JSON.stringify(newState));
    return newState;
  },

  [ADMIN_ACTION_TYPES.SET_PARTS]: (state, action) => {
    const newState = { ...state, parts: action.payload };
    window.localStorage.setItem("admin", JSON.stringify(newState));
    return newState;
  },

  [ADMIN_ACTION_TYPES.SET_RULE]: (state, action) => {
    const newState = { ...state, configurationRules: action.payload };
    window.localStorage.setItem("admin", JSON.stringify(newState));
    return newState;
  },
  [ADMIN_ACTION_TYPES.ADD_PRODUCT]: (state, action) => {
    const newState = {
      ...state,
      products: [...state.products, action.payload],
    };
    window.localStorage.setItem("admin", JSON.stringify(newState));
    return newState;
  },
  [ADMIN_ACTION_TYPES.ADD_PART]: (state, action) => {
    const newState = {
      ...state,
      parts: [...state.parts, action.payload],
    };
    window.localStorage.setItem("admin", JSON.stringify(newState));
    return newState;
  },
  [ADMIN_ACTION_TYPES.ADD_RULE]: (state, action) => {
    const newState = {
      ...state,
      configurationRules: [...state.configurationRules, action.payload],
    };
    window.localStorage.setItem("admin", JSON.stringify(newState));
    return newState;
  },
};

export const adminReducer = (state, action) => {
  const { type: actionType } = action;
  const updateState = UPDATE_STATE_BY_ACTION[actionType];
  return updateState ? updateState(state, action) : state;
};
