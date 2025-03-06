import React, { createContext, useReducer, useEffect } from "react";
import {
  setAuthToken,
  login as loginService,
  logout as logoutService,
  user as userService,
} from "../services.js";

export const AuthContext = createContext();

const initialState = {
  isAuthenticated: false,
  user: null,
  token: null,
};

const authReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN_SUCCESS":
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
      };
    case "LOGOUT":
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
      };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setAuthToken(token);
      fetchUserAndDispatch(token);
    }
  }, []);

  const fetchUserAndDispatch = async (token) => {
    const user = await userService();
    dispatch({ type: "LOGIN_SUCCESS", payload: { user, token } });
    localStorage.setItem("user", JSON.stringify(user));
  };

  const login = async (username, password) => {
    const access_token = await loginService(username, password);
    if (access_token) {
      localStorage.setItem("token", access_token);
      setAuthToken(access_token);
      await fetchUserAndDispatch(access_token);
    }
  };

  const logout = async () => {
    await logoutService();
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setAuthToken(null);
    dispatch({ type: "LOGOUT" });
  };

  return (
    <AuthContext.Provider value={{ state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
