import React, { useState } from "react";
import { createProduct, deleteProduct } from "../services";

const AdminDashboard = () => {
  const [productName, setProductName] = useState("");
  const [productCategory, setProductCategory] = useState("");
  const [productId, setProductId] = useState("");

  const handleCreateProduct = async () => {
    try {
      const product = {
        product_id: productId,
        name: productName,
        category: productCategory,
        available_parts: [],
        configuration_rules: [],
      };
      await createProduct(product);
      alert("Product created");
    } catch (error) {
      alert("Failed to create product");
    }
  };

  const handleDeleteProduct = async () => {
    try {
      await deleteProduct(productId);
      alert("Product deleted");
    } catch (error) {
      alert("Failed to delete product");
    }
  };

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div>
        <h2>Create Product</h2>
        <input
          type="text"
          placeholder="Product ID"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        />
        <input
          type="text"
          placeholder="Product Name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Product Category"
          value={productCategory}
          onChange={(e) => setProductCategory(e.target.value)}
        />
        <button onClick={handleCreateProduct}>Create Product</button>
      </div>
      <div>
        <h2>Delete Product</h2>
        <input
          type="text"
          placeholder="Product ID"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        />
        <button onClick={handleDeleteProduct}>Delete Product</button>
      </div>
    </div>
  );
};

export default AdminDashboard;
