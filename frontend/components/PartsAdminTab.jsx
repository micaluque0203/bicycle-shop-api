import { useEffect, useState } from "react";
import { useAdmin } from "../hooks/useAdmin.jsx";
import AdminTabHeader from "./AdminTabHeader";
import AdminTabTable from "./AdminTabTable";
import AdminModal from "../components/AdminModal";

const PartsAdminTab = () => {
  const categories = ["Frame", "Wheels", "Saddle", "Rim", "Pedals", "Chain"];

  const columns = [
    { Header: "Name", accessor: "name" },
    { Header: "Type", accessor: "part_type" },
    {
      Header: "Stock Status",
      accessor: "stock_status",
    },
  ];

  const { admin_dash, fetchParts, addPart } = useAdmin();

  const [isOpen, setIsOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [currentPart, setCurrentPart] = useState({
    name: "",
    category: categories[0],
    stock_status: "available",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentPart({ ...currentPart, [name]: value });
  };

  const handleCategoryChange = (type) => {
    setCurrentPart({ ...currentPart, type });
  };

  const handleStatusChange = (stock_status) => {
    setCurrentPart({ ...currentPart, stock_status });
  };

  const openModal = (part = null) => {
    setIsEdit(part !== null);
    setCurrentPart(
      part || {
        name: "",
        category: categories[0],
        stock_status: "available",
      }
    );
    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      name: currentPart.name,
      part_type: currentPart.category,
      stock_status: currentPart.stock_status,
    };
    try {
      if (isEdit) {
        // Update product endpoint (if available)
        // await updateProduct(payload);
        // fetchProducts();
      } else {
        await addPart(payload);
        fetchParts();
      }
      closeModal();
    } catch (error) {
      console.error("Error submitting product:", error);
    }
  };

  useEffect(() => {
    async function fetchData() {
      if (admin_dash.parts.length === 0) {
        await fetchParts();
      }
    }
    fetchData();
  }, [admin_dash.parts]);

  return (
    <div>
      <AdminTabHeader
        title="Parts"
        description="A list of all the parts in your shop."
        buttonText="Add part"
        onButtonClick={() => openModal()}
      />
      <AdminTabTable
        columns={columns}
        data={admin_dash.parts}
        onEditClick={openModal}
      />
      <AdminModal
        isOpen={isOpen}
        onClose={closeModal}
        isEdit={isEdit}
        entity="Part"
        stock_status={["available", "out_of_stock"]}
        categories={categories}
        currentEntity={currentPart}
        handleInputChange={handleInputChange}
        handleCategoryChange={handleCategoryChange}
        handleSubmit={handleSubmit}
        handleStatusChange={handleStatusChange}
      />
    </div>
  );
};

export default PartsAdminTab;
