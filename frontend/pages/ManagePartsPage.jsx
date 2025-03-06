import React, { useState, useEffect } from "react";
import { fetchProduct, updateProductParts } from "../services";
import { useParams } from "react-router-dom";

const ManageParts = () => {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [partType, setPartType] = useState("");
  const [partName, setPartName] = useState("");
  const [partStockStatus, setPartStockStatus] = useState("available");

  useEffect(() => {
    const getProduct = async () => {
      const product = await fetchProduct(productId);
      setProduct(product);
    };
    getProduct();
  }, [productId]);

  const handleAddPart = async () => {
    const newPart = {
      part_type: partType,
      name: partName,
      stock_status: partStockStatus,
    };
    const updatedParts = [...product.available_parts, newPart];
    await updateProductParts(productId, updatedParts);
    setProduct({ ...product, available_parts: updatedParts });
    setPartType("");
    setPartName("");
    setPartStockStatus("available");
  };

  if (!product) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Manage Parts for {product.name}</h1>
      <div>
        <input
          type="text"
          placeholder="Part Type"
          value={partType}
          onChange={(e) => setPartType(e.target.value)}
        />
        <input
          type="text"
          placeholder="Part Name"
          value={partName}
          onChange={(e) => setPartName(e.target.value)}
        />
        <select
          value={partStockStatus}
          onChange={(e) => setPartStockStatus(e.target.value)}
        >
          <option value="available">Available</option>
          <option value="out_of_stock">Out of Stock</option>
        </select>
        <button onClick={handleAddPart}>Add Part</button>
      </div>
      <div>
        <h2>Current Parts</h2>
        <ul>
          {product.available_parts.map((part) => (
            <li key={part.name}>
              {part.part_type}: {part.name} ({part.stock_status})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ManageParts;
