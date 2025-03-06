import { useEffect, useState } from "react";
import { useAdmin } from "../hooks/useAdmin.jsx";
import AdminTabHeader from "./AdminTabHeader";
import AdminTabTable from "./AdminTabTable";
import AdminModal from "../components/AdminModal";

const OptionsAdminTab = () => {
  const categories = ["Frame", "Wheels", "Saddle", "Rim", "Pedals", "Chain"];

  const forbidden_values = ["diamond", "platinum", "gold", "silver", "bronze"];

  const columns = [
    { Header: "Depends on", accessor: "depends_on" },
    { Header: "Depends value", accessor: "depends_value" },
    {
      Header: "Forbidden values",
      accessor: "forbidden_values",
    },
  ];

  const { admin_dash, fetchRules, addRule } = useAdmin();

  const [isOpen, setIsOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [currentOption, setCurrentOption] = useState({
    depends_on: categories[1],
    depends_value: "",
    forbidden_values: [],
  });

  const openModal = (rule = null) => {
    setIsEdit(rule !== null);
    setCurrentOption(
      rule || {
        depends_on: categories[0],
        depends_value: "",
        forbidden_values: [],
      }
    );
    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentOption({ ...currentOption, depends_value: value });
  };

  const handleCategoryChange = (depends_on) => {
    setCurrentOption({ ...currentOption, depends_on });
  };

  const handleForbiddenValuesChange = (newValues) => {
    setCurrentOption({
      ...currentOption,
      forbidden_values: newValues,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      depends_on: currentOption.depends_on,
      depends_value: currentOption.depends_value,
      forbidden_values: currentOption.forbidden_values,
    };
    try {
      if (isEdit) {
        // Update product endpoint (if available)
        // await updateProduct(payload);
        // fetchProducts();
      } else {
        await addRule(payload);
        fetchRules();
      }
      closeModal();
    } catch (error) {
      console.error("Error submitting option:", error);
    }
  };

  useEffect(() => {
    async function fetchData() {
      if (admin_dash.configurationRules.length === 0) {
        await fetchRules();
      }
    }
    fetchData();
  }, [admin_dash.configurationRules]);

  return (
    <div>
      <AdminTabHeader
        title="Options"
        description="A list of all the configuration rules in your shop."
        buttonText="Add rule"
        onButtonClick={() => openModal()}
      />
      <AdminTabTable
        columns={columns}
        data={admin_dash.configurationRules}
        onEditClick={openModal}
      />
      <AdminModal
        isOpen={isOpen}
        onClose={closeModal}
        isEdit={isEdit}
        entity="Rule"
        categories={categories}
        currentEntity={currentOption}
        handleInputChange={handleInputChange}
        handleCategoryChange={handleCategoryChange}
        handleSubmit={handleSubmit}
        handleForbiddenValuesChange={handleForbiddenValuesChange}
        forbidden_values={forbidden_values}
      />
    </div>
  );
};

export default OptionsAdminTab;
