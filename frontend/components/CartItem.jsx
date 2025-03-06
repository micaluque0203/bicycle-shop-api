import { ChevronDownIcon } from "@heroicons/react/16/solid";
import {
  CheckIcon,
  ClockIcon,
  QuestionMarkCircleIcon,
  XMarkIcon as XMarkIconMini,
} from "@heroicons/react/20/solid";

export default function ({ key, id, name, category, quantity, configuration }) {
  return (
    <li key={key} className="flex items-center py-6">
      <img
        alt={name}
        src="/assets/josh-nuttall-zkVi57UYHIQ-unsplash.jpg"
        className="size-16 flex-none rounded-md border border-gray-200"
      />
      <div className="ml-4 flex flex-1 flex-col justify-between sm:ml-6">
        <div>
          <h3 className="font-medium text-gray-900">
            <a href={`/product/${id}`}>{name}</a>
          </h3>
          <p className="text-gray-700">
            {category} - Quantity {quantity}
          </p>
          <div>
            <p className="text-gray-500 text-xs">
              {configuration.map((item, index) => {
                const key = Object.keys(item)[0];
                const value = item[key];
                return <span key={index}>{value} | </span>;
              })}
            </p>
          </div>
        </div>
      </div>
    </li>
  );
}
