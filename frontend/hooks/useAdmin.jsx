import { AdminContext } from "../context/admin.jsx";
import { useContext } from "react";

export const useAdmin = () => {
  const context = useContext(AdminContext);
  if (context === undefined) {
    throw new Error("useAdmin must be used within a AdminProvider");
  }

  return context;
};
