import { useState } from "react";
import MobileMenu from "./MobileMenu.jsx";
import {
  Popover,
  PopoverButton,
  PopoverGroup,
  PopoverPanel,
} from "@headlessui/react";
import {
  Bars3Icon,
  MagnifyingGlassIcon,
  ShoppingBagIcon,
  UserIcon,
  XMarkIcon as XMarkIconOutline,
} from "@heroicons/react/24/outline";
import { Cart } from "../components/Cart.jsx";
import { useAuth } from "../hooks/useAuth.jsx";

import LogoImg from "./Logo.jsx";

export function Header() {
  const [open, setOpen] = useState(false);
  const { state, login, logout } = useAuth();
  const navigation = {
    categories: [
      {
        id: "new-in",
        name: "New In",
        featured: [
          {
            name: "Bikes",
            href: "#",
            imageSrc: "/assets/david-dvoracek-_2LOMg2B_EQ-unsplash.jpg",
            imageAlt:
              "Models sitting back to back, wearing Basic Tee in black and bone.",
          },
          {
            name: "Accesories",
            href: "#",
            imageSrc: "/assets/jan-kopriva-dJuCkofVIR8-unsplash.jpg",
            imageAlt:
              "Close up of Basic Tee fall bundle with off-white, ochre, olive, and black tees.",
          },
        ],
        sections: [
          {
            id: "bikes",
            name: "Bikes",
            items: [
              { name: "MTB", href: "#" },
              { name: "Gravel", href: "#" },
              { name: "Road", href: "#" },
              { name: "E-Bike", href: "#" },
            ],
          },
          {
            id: "accessories",
            name: "Accessories",
            items: [
              { name: "Helmets", href: "#" },
              { name: "Socks", href: "#" },
              { name: "Bags", href: "#" },
              { name: "Sunglasses", href: "#" },
              { name: "Shoes", href: "#" },
              { name: "Belts", href: "#" },
            ],
          },
          {
            id: "brands",
            name: "Brands",
            items: [
              { name: "Cannondale", href: "#" },
              { name: "Poc", href: "#" },
              { name: "Specialized", href: "#" },
              { name: "Trek", href: "#" },
              { name: "Focus", href: "#" },
            ],
          },
        ],
      },
    ],
    pages: [
      { name: "Company", href: "#" },
      { name: "Stores", href: "#" },
    ],
  };
  return (
    <div className="bg-white">
      <MobileMenu open={open} setOpen={setOpen} />
      <header className="relative bg-white">
        <p className="flex h-10 items-center justify-center bg-blue-600 px-4 text-sm font-medium text-white sm:px-6 lg:px-8">
          Get free delivery on orders over $100
        </p>

        <nav
          aria-label="Top"
          className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"
        >
          <div className="border-b border-gray-200">
            <div className="flex h-16 items-center">
              <button
                type="button"
                onClick={() => setOpen(true)}
                className="relative rounded-md bg-white p-2 text-gray-400 lg:hidden"
              >
                <span className="absolute -inset-0.5" />
                <span className="sr-only">Open menu</span>
                <Bars3Icon aria-hidden="true" className="size-6" />
              </button>

              {/* Logo */}
              <div className="ml-4 flex lg:ml-0">
                <LogoImg></LogoImg>
              </div>

              {/* Flyout menus */}
              <PopoverGroup className="hidden lg:ml-8 lg:block lg:self-stretch">
                <div className="flex h-full space-x-8">
                  {navigation.categories.map((category) => (
                    <Popover key={category.name} className="flex">
                      <div className="relative flex">
                        <PopoverButton className="relative z-10 -mb-px flex items-center border-b-2 border-transparent pt-px text-sm font-medium text-gray-700 transition-colors duration-200 ease-out hover:text-gray-800 data-open:border-blue-600 data-open:text-blue-600">
                          {category.name}
                        </PopoverButton>
                      </div>

                      <PopoverPanel
                        transition
                        className="absolute inset-x-0 top-full z-10 text-sm text-gray-500 transition data-closed:opacity-0 data-enter:duration-200 data-enter:ease-out data-leave:duration-150 data-leave:ease-in"
                      >
                        {/* Presentational element used to render the bottom shadow, if we put the shadow on the actual panel it pokes out the top, so we use this shorter element to hide the top of the shadow */}
                        <div
                          aria-hidden="true"
                          className="absolute inset-0 top-1/2 bg-white shadow-sm"
                        />

                        <div className="relative bg-white">
                          <div className="mx-auto max-w-7xl px-8">
                            <div className="grid grid-cols-2 gap-x-8 gap-y-10 py-16">
                              <div className="col-start-2 grid grid-cols-2 gap-x-8">
                                {category.featured.map((item) => (
                                  <div
                                    key={item.name}
                                    className="group relative text-base sm:text-sm"
                                  >
                                    <img
                                      alt={item.imageAlt}
                                      src={item.imageSrc}
                                      className="aspect-square w-full rounded-lg bg-gray-100 object-cover group-hover:opacity-75"
                                    />
                                    <a
                                      href={item.href}
                                      className="mt-6 block font-medium text-gray-900"
                                    >
                                      <span
                                        aria-hidden="true"
                                        className="absolute inset-0 z-10"
                                      />
                                      {item.name}
                                    </a>
                                    <p aria-hidden="true" className="mt-1">
                                      Shop now
                                    </p>
                                  </div>
                                ))}
                              </div>
                              <div className="row-start-1 grid grid-cols-3 gap-x-8 gap-y-10 text-sm">
                                {category.sections.map((section) => (
                                  <div key={section.name}>
                                    <p
                                      id={`${section.name}-heading`}
                                      className="font-medium text-gray-900"
                                    >
                                      {section.name}
                                    </p>
                                    <ul
                                      role="list"
                                      aria-labelledby={`${section.name}-heading`}
                                      className="mt-6 space-y-6 sm:mt-4 sm:space-y-4"
                                    >
                                      {section.items.map((item) => (
                                        <li key={item.name} className="flex">
                                          <a
                                            href={item.href}
                                            className="hover:text-gray-800"
                                          >
                                            {item.name}
                                          </a>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </PopoverPanel>
                    </Popover>
                  ))}

                  {navigation.pages.map((page) => (
                    <a
                      key={page.name}
                      href={page.href}
                      className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-800"
                    >
                      {page.name}
                    </a>
                  ))}
                </div>
              </PopoverGroup>

              <div className="ml-auto flex items-center">
                {!state.isAuthenticated && (
                  <div className="hidden lg:flex lg:flex-1 lg:items-center lg:justify-end lg:space-x-6">
                    <a
                      href="/login"
                      className="text-sm font-medium text-gray-700 hover:text-gray-800"
                    >
                      Sign in
                    </a>
                    <span aria-hidden="true" className="h-6 w-px bg-gray-200" />
                    <a
                      href="/register"
                      className="text-sm font-medium text-gray-700 hover:text-gray-800"
                    >
                      Create account
                    </a>
                  </div>
                )}
                {state.isAuthenticated && (
                  <div className="hidden lg:flex lg:flex-1 lg:items-center lg:justify-end lg:space-x-6">
                    <button
                      onClick={logout}
                      className="text-sm font-medium text-gray-700 hover:text-gray-800"
                    >
                      Logout
                    </button>
                  </div>
                )}

                {state.isAuthenticated && state.user.is_superuser && (
                  <div className="flex lg:ml-6">
                    <a
                      href="/admin"
                      className="p-2 text-gray-400 hover:text-gray-500"
                    >
                      <span className="sr-only">Admin Dashboard</span>
                      <UserIcon aria-hidden="true" className="size-6" />
                    </a>
                  </div>
                )}
                <Cart />
              </div>
            </div>
          </div>
        </nav>
      </header>
    </div>
  );
}
