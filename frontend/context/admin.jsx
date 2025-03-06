import React, { createContext, useReducer } from "react";

import { adminReducer } from "../reducers/admin.js";
import {
  fetchParts as fetchPartsService,
  fetchProducts as fetchProductsService,
  fetchRules as fetchConfigurationRules,
  createProduct,
  createPart,
  createRule,
} from "../services";

export const AdminContext = createContext();

const initialState = {
  products: [],
  parts: [],
  configurationRules: [],
};

const adminInitialState =
  JSON.parse(window.localStorage.getItem("admin")) || initialState;

function useAdminReducer() {
  const [state, dispatch] = useReducer(adminReducer, adminInitialState);

  const fetchParts = async () => {
    const parts = await fetchPartsService();
    dispatch({ type: "SET_PARTS", payload: parts });
  };

  const fetchProducts = async () => {
    const products = await fetchProductsService();
    console.log(products);
    dispatch({ type: "SET_PRODUCTS", payload: products });
  };

  const fetchRules = async () => {
    const configurationRules = await fetchConfigurationRules();
    console.log(configurationRules);
    dispatch({ type: "SET_RULE", payload: configurationRules });
  };

  const addProduct = async (product) => {
    const newProduct = await createProduct(product);
    dispatch({ type: "ADD_PRODUCT", payload: newProduct });
  };

  const addPart = async (part) => {
    const newPart = await createPart(part);
    dispatch({ type: "ADD_PART", payload: newPart });
  };

  const addRule = async (rule) => {
    const newPart = await createRule(rule);
    dispatch({ type: "ADD_RULE", payload: newPart });
  };

  return {
    state,
    fetchParts,
    fetchProducts,
    fetchRules,
    addProduct,
    addPart,
    addRule,
  };
}

export const AdminProvider = ({ children }) => {
  const {
    state,
    fetchParts,
    fetchProducts,
    fetchRules,
    addProduct,
    addPart,
    addRule,
  } = useAdminReducer();

  return (
    <AdminContext.Provider
      value={{
        admin_dash: state,
        fetchParts,
        fetchProducts,
        fetchRules,
        addProduct,
        addPart,
        addRule,
      }}
    >
      {children}
    </AdminContext.Provider>
  );
};
