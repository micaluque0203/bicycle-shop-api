import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8001",
  withCredentials: true,
});

export const register = async (email, password) => {
  const response = await api.post("/auth/register", { email, password });
  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post(
    "/auth/jwt/login",
    new URLSearchParams({
      grant_type: "password",
      username: username,
      password: password,
    }),
    {
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  const { access_token } = response.data;
  setAuthToken(access_token);

  return access_token;
};

export const user = async () => {
  const response = await api.get("/users/me");
  return response.data;
};

export const logout = async () => {
  const response = await api.post("/auth/jwt/logout");
  return response.data;
};

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
};

export const fetchProducts = async () => {
  const response = await api.get("/products");
  return response.data;
};

export const fetchProduct = async (productId) => {
  const response = await api.get(`/products/${productId}`);
  return response.data;
};

export const fetchRules = async () => {
  const response = await api.get(`/admin/configuration-rules`);
  return response.data;
};

export const fetchParts = async () => {
  const response = await api.get("/admin/parts");
  return response.data;
};

export const addToCart = async (options, productId) => {
  const response = await api.post(`/cart?product_id=${productId}`, {
    options,
  });
  return response.data;
};

export const fetchCart = async () => {
  const response = await api.get("/cart");
  return response.data;
};

export const createProduct = async (product) => {
  const response = await api.post("/admin/products", product);
  return response.data;
};

export const createPart = async (parts) => {
  const response = await api.post("/admin/parts", parts);
  return response.data;
};

export const createRule = async (rule) => {
  const response = await api.post("/admin/configuration-rules", rule);
  return response.data;
};

export const validateOrderItem = async (configuration, product_id) => {
  // configuration, product_id
  const response = await api.post(
    "/validate-order-item",
    configuration,
    product_id
  );
  return response.data;
};

export const deleteProduct = async (productId) => {
  const response = await api.delete(`/admin/products/${productId}`);
  return response.data;
};

export const updateProductParts = async (productId, parts) => {
  const response = await api.put(`/admin/products/${productId}/parts`, parts);
  return response.data;
};
