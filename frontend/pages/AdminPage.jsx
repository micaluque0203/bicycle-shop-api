import { useState, React } from "react";
import {
  CubeIcon,
  UserCircleIcon,
  CogIcon,
  WrenchIcon,
} from "@heroicons/react/24/outline";
import ProductsAdminTab from "../components/ProductsAdminTab.jsx";
import PartsAdminTab from "../components/PartsAdminTab.jsx";
import OptionsAdminTab from "../components/OptionsAdminTab.jsx";
import { useAuth } from "../hooks/useAuth.jsx";
import { useNavigate } from "react-router-dom";

const initialSecondaryNavigation = [
  { name: "General", href: "#", icon: UserCircleIcon, current: true },
  { name: "Products", href: "#", icon: CubeIcon, current: false },
  { name: "Parts", href: "#", icon: WrenchIcon, current: false },
  { name: "Options", href: "#", icon: CogIcon, current: false },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export function AdminPage() {
  const navigateTo = useNavigate();
  const { state, logout } = useAuth();
  const [activeTab, setActiveTab] = useState("General");
  const [secondaryNavigation, setSecondaryNavigation] = useState(
    initialSecondaryNavigation
  );

  const renderContent = () => {
    switch (activeTab) {
      case "Products":
        return <ProductsAdminTab />;
      case "Parts":
        return <PartsAdminTab />;
      case "Options":
        return <OptionsAdminTab />;
      default:
        return <div>Welcome!</div>;
    }
  };

  const handleTabClick = (name) => {
    setActiveTab(name);
    setSecondaryNavigation(
      secondaryNavigation.map((item) => ({
        ...item,
        current: item.name === name,
      }))
    );
  };

  if (!state.isAuthenticated) {
    navigateTo("/login");
  }

  return (
    <div className="mx-auto max-w-7xl pt-16 lg:flex lg:gap-x-16 lg:px-8">
      <aside className="flex overflow-x-auto border-b border-gray-900/5 py-4 lg:block lg:w-64 lg:flex-none lg:border-0 lg:py-20">
        <nav className="flex-none px-4 sm:px-6 lg:px-0">
          <ul
            role="list"
            className="flex gap-x-3 gap-y-1 whitespace-nowrap lg:flex-col"
          >
            {secondaryNavigation.map((item) => (
              <li key={item.name}>
                <button
                  onClick={() => handleTabClick(item.name)}
                  className={classNames(
                    item.current
                      ? "bg-gray-50 text-blue-600"
                      : "text-gray-700 hover:bg-gray-50 hover:text-blue-600",
                    "group flex gap-x-3 rounded-md py-2 pr-3 pl-2 text-sm/6 font-semibold"
                  )}
                >
                  <item.icon
                    aria-hidden="true"
                    className={classNames(
                      item.current
                        ? "text-blue-600"
                        : "text-gray-400 group-hover:text-blue-600",
                      "size-6 shrink-0"
                    )}
                  />
                  {item.name}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      <main className="px-4 py-16 sm:px-6 lg:flex-auto lg:px-0 lg:py-20">
        <div className="mx-auto max-w-2xl space-y-16 sm:space-y-20 lg:mx-0 lg:max-w-none">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
