import React, { Fragment } from "react";
import {
  DialogPanel,
  TransitionChild,
  Dialog,
  DialogTitle,
  Transition,
} from "@headlessui/react";
import MultiSelectDropdown from "./AdminMultiSelectDropdown.jsx";
import Dropdown from "./AdminDropdown.jsx";

const AdminModal = ({
  isOpen,
  onClose,
  isEdit,
  entity,
  categories,
  currentEntity,
  handleInputChange,
  handleCategoryChange,
  handlePartChange,
  handleConfigurationRuleChange,
  handleSubmit,
  parts,
  configurationRules,
  handleStatusChange,
  stock_status,
  handleForbiddenValuesChange,
  forbidden_values,
}) => {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <TransitionChild
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <DialogPanel className="w-full max-w-md transform rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle
                  as="h3"
                  className="text-lg font-medium leading-6 text-gray-900"
                >
                  {isEdit ? `Edit ${entity}` : `Add ${entity}`}
                </DialogTitle>
                <form onSubmit={handleSubmit}>
                  {categories && "Rule" === entity && (
                    <Dropdown
                      label="Depends On"
                      value={currentEntity.depends_on}
                      options={categories}
                      onChange={handleCategoryChange}
                    />
                  )}
                  <div className="mt-2">
                    <label
                      htmlFor="name"
                      className="block text-sm font-medium text-gray-700"
                    >
                      {"Rule" === entity ? "Depends value" : "Name"}
                    </label>
                    <input
                      type="text"
                      name="name"
                      id="name"
                      value={
                        "Rule" === entity
                          ? currentEntity.depends_value
                          : currentEntity.name
                      }
                      onChange={handleInputChange}
                      className="mt-1 block w-full py-2 pl-3 pr-10 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      required
                    />
                  </div>
                  {stock_status && (
                    <Dropdown
                      label="Stock Status"
                      value={currentEntity.stock_status}
                      options={stock_status}
                      onChange={handleStatusChange}
                    />
                  )}
                  {categories && "Rule" !== entity && (
                    <Dropdown
                      label="Category"
                      value={currentEntity.category}
                      options={categories}
                      onChange={handleCategoryChange}
                    />
                  )}
                  {parts && (
                    <MultiSelectDropdown
                      options={parts.map((part) => part.name)}
                      selectedOptions={currentEntity.parts}
                      onChange={handlePartChange}
                      label="Parts"
                    />
                  )}
                  {configurationRules && (
                    <MultiSelectDropdown
                      options={configurationRules.map((rule) => rule.name)}
                      selectedOptions={currentEntity.configurationRules}
                      onChange={handleConfigurationRuleChange}
                      label="Configuration Rules"
                    />
                  )}
                  {forbidden_values && (
                    <MultiSelectDropdown
                      options={forbidden_values}
                      selectedOptions={currentEntity.forbidden_values}
                      onChange={handleForbiddenValuesChange}
                      label="Forbidden Values"
                    />
                  )}

                  <div className="mt-4">
                    <button
                      type="submit"
                      className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    >
                      {isEdit ? "Update" : "Add"}
                    </button>
                    <button
                      type="button"
                      className="ml-2 inline-flex justify-center rounded-md border border-transparent bg-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                      onClick={onClose}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
};

export default AdminModal;
