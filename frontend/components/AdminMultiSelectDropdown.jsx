import React from "react";
import Select from "react-select";

const MultiSelectDropdown = ({ options, selectedOptions, onChange, label }) => {
  const formattedOptions = options.map((option) => ({
    value: option,
    label: option,
  }));

  return (
    <div className="mt-2">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <Select
        isMulti
        closeMenuOnSelect={false}
        options={formattedOptions}
        onChange={(selectedOptions) =>
          onChange(
            selectedOptions ? selectedOptions.map((option) => option.value) : []
          )
        }
        className="mt-1 block w-full"
      />
    </div>
  );
};

export default MultiSelectDropdown;
