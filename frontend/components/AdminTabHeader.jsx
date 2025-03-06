import React from "react";

const AdminTabHeader = ({ title, description, buttonText, onButtonClick }) => {
  return (
    <div className="sm:flex sm:items-center">
      <div className="sm:flex-auto">
        <h1 className="text-base font-semibold text-gray-900">{title}</h1>
        <p className="mt-2 text-sm text-gray-700">{description}</p>
      </div>
      <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <button
          type="button"
          onClick={onButtonClick}
          className="block rounded-md bg-blue-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-xs hover:bg-blue-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
          {buttonText}
        </button>
      </div>
    </div>
  );
};

export default AdminTabHeader;
