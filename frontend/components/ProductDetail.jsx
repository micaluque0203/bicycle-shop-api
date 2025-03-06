import React, { useEffect, useState } from "react";
import { fetchProduct } from "../services";
import { Radio, RadioGroup, Listbox } from "@headlessui/react";
import { CheckIcon, ChevronDownIcon } from "@heroicons/react/20/solid";
import { useParams } from "react-router-dom";
import { useCart } from "../hooks/useCart.jsx";

const ProductDetail = () => {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [configuration, setConfiguration] = useState({});
  const [selectedParts, setSelectedParts] = useState({});

  const { addToCart } = useCart();

  function classNames(...classes) {
    return classes.filter(Boolean).join(" ");
  }

  useEffect(() => {
    const getProduct = async () => {
      const product = await fetchProduct(productId);
      setProduct(product);
    };
    getProduct();
  }, [productId]);

  const handleOptionChange = (partType, partName) => {
    setConfiguration((prev) => ({ ...prev, [partType]: partName }));
    setSelectedParts((prev) => ({ ...prev, [partType]: partName }));
  };

  const handleAddToCart = async () => {
    const formattedConfiguration = Object.entries(configuration).map(
      ([key, value]) => ({ [key]: value })
    );

    try {
      await addToCart({
        product,
        productId,
        configuration: formattedConfiguration,
      });
      alert("Added to cart");
    } catch (error) {
      alert(error.message);
    }
  };

  if (!product) {
    return <div className="text-xl font-medium text-gray-900">Loading...</div>;
  }

  const imgPlaceholder = [
    "/assets/mikkel-bech-yjAFnkLtKY0-unsplash (1).jpg",
    "/assets/josh-nuttall-XVTWFHcNIko-unsplash.jpg",
    "/assets/josh-nuttall-zkVi57UYHIQ-unsplash.jpg",
  ];

  const colorVariants = {
    blue: "bg-blue-600",
    red: "bg-red-600",
    black: "bg-black",
  };

  const availablePartsByType = product.available_parts.reduce((acc, part) => {
    if (!acc[part.part_type]) {
      acc[part.part_type] = [];
    }
    acc[part.part_type].push(part);
    return acc;
  }, {});

  return (
    <div className="bg-white">
      <main className="mx-auto mt-8 max-w-2xl px-4 pb-16 sm:px-6 sm:pb-24 lg:max-w-7xl lg:px-8">
        <div className="lg:grid lg:auto-rows-min lg:grid-cols-12 lg:gap-x-8">
          <div className="lg:col-span-5 lg:col-start-8">
            <div className="flex justify-between">
              <h1 className="text-xl font-medium text-gray-900">
                {product.name}
              </h1>
              <p className="text-xl font-medium text-gray-900">
                {product.price}
              </p>
            </div>
          </div>

          <div className="mt-8 lg:col-span-7 lg:col-start-1 lg:row-span-3 lg:row-start-1 lg:mt-0">
            <h2 className="sr-only">Images</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 lg:grid-rows-3 lg:gap-8">
              {imgPlaceholder.map((image, index) => (
                <img
                  key={index}
                  src={image}
                  className={classNames(
                    index === 0
                      ? "lg:col-span-2 lg:row-span-2"
                      : "hidden lg:block",
                    "rounded-lg"
                  )}
                />
              ))}
            </div>
          </div>
          <div className="mt-8 lg:col-span-5">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleAddToCart();
              }}
            >
              {Object.keys(availablePartsByType).map((partType) => (
                <div key={partType} className="mt-8">
                  <h2 className="text-sm font-medium text-gray-900">
                    {partType}
                  </h2>
                  {partType === "Rim color" || partType === "Frame color" ? (
                    <fieldset
                      aria-label={`Choose a ${partType}`}
                      className="mt-2"
                    >
                      <RadioGroup
                        value={configuration[partType]}
                        onChange={(partName) =>
                          handleOptionChange(partType, partName)
                        }
                        className="grid grid-cols-3 gap-3 sm:grid-cols-6"
                      >
                        {availablePartsByType[partType].map((part) => (
                          <Radio
                            key={part._id}
                            value={part.name}
                            disabled={part.stock_status !== "available"}
                            className={classNames(
                              part.stock_status === "available"
                                ? "cursor-pointer focus:outline-none"
                                : "cursor-not-allowed opacity-25",
                              configuration[partType] === part.name
                                ? "bg-blue-600 text-white"
                                : "bg-white text-gray-900",
                              "flex items-center justify-center rounded-md border border-gray-200 px-3 py-3 text-sm font-medium uppercase hover:bg-gray-50"
                            )}
                          >
                            <span
                              className={classNames(
                                colorVariants[part.name.toLowerCase()],
                                "size-8 rounded-full border border-black/10 focus:border-blue-500 focus:ring-blue-500"
                              )}
                              aria-hidden="true"
                            />
                          </Radio>
                        ))}
                      </RadioGroup>
                    </fieldset>
                  ) : (
                    <Listbox
                      value={configuration[partType]}
                      onChange={(partName) =>
                        handleOptionChange(partType, partName)
                      }
                    >
                      <div className="relative">
                        <Listbox.Button className="relative w-full cursor-pointer rounded-md bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-opacity-75 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-gray-300">
                          <span className="block truncate">
                            {configuration[partType] || `Choose a ${partType}`}
                          </span>
                          <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                            <ChevronDownIcon
                              className="h-5 w-5 text-gray-400"
                              aria-hidden="true"
                            />
                          </span>
                        </Listbox.Button>
                        <Listbox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                          {availablePartsByType[partType].map((part) => (
                            <Listbox.Option
                              key={part._id}
                              value={part.name}
                              disabled={part.stock_status !== "available"}
                              className={({ active }) =>
                                classNames(
                                  active
                                    ? "text-white bg-blue-600"
                                    : "text-gray-900",
                                  "relative cursor-default select-none py-2 pl-10 pr-4",
                                  part.stock_status !== "available" &&
                                    "opacity-25 cursor-not-allowed"
                                )
                              }
                            >
                              {({ selected }) => (
                                <>
                                  <span
                                    className={classNames(
                                      selected ? "font-medium" : "font-normal",
                                      "block truncate"
                                    )}
                                  >
                                    {part.name}
                                  </span>
                                  {selected ? (
                                    <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600">
                                      <CheckIcon
                                        className="h-5 w-5"
                                        aria-hidden="true"
                                      />
                                    </span>
                                  ) : null}
                                </>
                              )}
                            </Listbox.Option>
                          ))}
                        </Listbox.Options>
                      </div>
                    </Listbox>
                  )}
                </div>
              ))}
              <button
                type="submit"
                className={classNames(
                  "mt-8 flex w-full items-center justify-center rounded-md border border-transparent px-8 py-3 text-base font-medium text-white",
                  Object.keys(selectedParts).length > 0
                    ? "bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    : "bg-gray-400 cursor-not-allowed"
                )}
                disabled={Object.keys(selectedParts).length === 0}
              >
                Add to cart
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProductDetail;
