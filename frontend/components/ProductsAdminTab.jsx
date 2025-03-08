import { useState, useEffect } from "react";
import { deleteProduct, createProduct, updateProduct } from "../services";
import AdminTabHeader from "./AdminTabHeader";
import AdminTabTable from "./AdminTabTable";
import { useAdmin } from "../hooks/useAdmin.jsx";
import AdminModal from "../components/AdminModal";

const categories = ["Bikes", "Accessories", "Components"];

const ProductsAdminTab = () => {
  const { admin_dash, fetchProducts } = useAdmin();

  const [isOpen, setIsOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [currentProduct, setCurrentProduct] = useState({
    name: "",
    category: categories[0],
    parts: [],
    configurationRules: [],
  });

  useEffect(() => {
    async function fetchData() {
      if (admin_dash.products.length === 0) {
        await fetchProducts();
      }
    }
    fetchData();
  }, [admin_dash.products]);

  const onRemoveClick = async (product) => {
    try {
      await deleteProduct(product.product_id);
      fetchProducts();
    } catch (error) {
      console.error("Error deleting products:", error);
    }
  };

  const openModal = (product = null) => {
    console.log(product);
    setIsEdit(product !== null);
    setCurrentProduct(
      product || {
        name: "",
        category: categories[0],
        parts: [],
        configurationRules: [],
      }
    );

    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentProduct({ ...currentProduct, [name]: value });
  };

  const handleCategoryChange = (category) => {
    setCurrentProduct({ ...currentProduct, category });
  };

  const handlePartChange = (selectedParts) => {
    const selectedPartIds = selectedParts.map(
      (partName) =>
        admin_dash.parts.find(
          (part) => `${part.name} ${part.part_type}` === partName
        ).id
    );
    setCurrentProduct({ ...currentProduct, parts: selectedPartIds });
  };

  const handleConfigurationRuleChange = (selectedRules) => {
    const selectedRuleIds = selectedRules.map(
      (ruleName) =>
        admin_dash.configurationRules.find(
          (rule) => `${rule.depends_on}: ${rule.depends_value}` === ruleName
        ).id
    );
    setCurrentProduct({
      ...currentProduct,
      configurationRules: selectedRuleIds,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      name: currentProduct.name,
      category: currentProduct.category,
      part_ids: currentProduct.parts,
      configuration_rule_ids: currentProduct.configurationRules,
    };
    try {
      if (isEdit) {
        await updateProduct(currentProduct.product_id, payload);
        fetchProducts();
      } else {
        await createProduct(payload);
        fetchProducts();
      }
      closeModal();
    } catch (error) {
      console.error("Error submitting product:", error);
    }
  };

  const columns = [
    { Header: "Name", accessor: "name" },
    { Header: "Category", accessor: "category" },
    {
      Header: "Parts",
      accessor: (row) =>
        row.available_parts.map((part) => part.name).join(", "),
    },
    {
      Header: "Configuration Rules",
      accessor: (row) =>
        row.configuration_rules
          .map((rule) => `${rule.depends_on}: ${rule.depends_value}`)
          .join(", "),
    },
    { Header: "Price", accessor: "price" },
  ];

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <AdminTabHeader
        title="Products"
        description="A list of all the products in your shop."
        buttonText="Add product"
        onButtonClick={() => openModal()}
      />
      <AdminTabTable
        columns={columns}
        data={admin_dash.products}
        onEditClick={openModal}
        onRemoveClick={onRemoveClick}
      />
      <AdminModal
        isOpen={isOpen}
        onClose={closeModal}
        isEdit={isEdit}
        entity="Product"
        categories={categories}
        currentEntity={currentProduct}
        handleInputChange={handleInputChange}
        handleCategoryChange={handleCategoryChange}
        handlePartChange={handlePartChange}
        handleConfigurationRuleChange={handleConfigurationRuleChange}
        handleSubmit={handleSubmit}
        parts={admin_dash.parts.map((part) => ({
          id: part.id,
          name: `${part.name} ${part.part_type}`,
        }))}
        configurationRules={admin_dash.configurationRules.map((rule) => ({
          id: rule.id,
          name: `${rule.depends_on}: ${rule.depends_value}`,
        }))}
      />
    </div>
  );
};

export default ProductsAdminTab;
