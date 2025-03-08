import React, { useId } from "react";

const AdminTabTable = ({ columns, data, onEditClick, onRemoveClick }) => (
  <div className="mt-8 flow-root">
    <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div className="overflow-hidden ring-1 shadow-sm ring-black/5 sm:rounded-lg">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                {columns.map((column) => {
                  const id = useId();
                  return (
                    <th
                      key={id}
                      scope="col"
                      className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                    >
                      {column.Header}
                    </th>
                  );
                })}
                <th
                  scope="col"
                  className="relative py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                >
                  <span className="sr-only">Edit</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {data.map((row) => (
                <tr key={row.id}>
                  {columns.map((column) => (
                    <td
                      key={column.accessor}
                      className="px-3 py-4 text-sm text-gray-500"
                    >
                      {typeof column.accessor === "function"
                        ? column.accessor(row)
                        : row[column.accessor]}
                    </td>
                  ))}
                  <td className="relative py-4 px-3 text-right text-sm font-medium whitespace-nowrap">
                    <button
                      onClick={() => onEditClick(row)}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      Edit
                      <span className="sr-only">, {row.id}</span>
                    </button>
                  </td>
                  <td className="relative py-4 px-3 text-right text-sm font-medium whitespace-nowrap">
                    <button
                      onClick={() => onRemoveClick(row)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Remove
                      <span className="sr-only">{row.id}</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
);

export default AdminTabTable;
