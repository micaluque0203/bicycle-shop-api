export default function ProductsList({ products }) {
  const topProducts = products.slice(0, 3);
  const imgPlaceholder = [
    "/assets/mikkel-bech-yjAFnkLtKY0-unsplash (1).jpg",
    "/assets/josh-nuttall-XVTWFHcNIko-unsplash.jpg",
    "/assets/patrick-hendry-OZh_OBP_fao-unsplash.jpg",
  ];

  return (
    <div className="bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="sm:flex sm:items-baseline sm:justify-between">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">
            Bikes
          </h2>
          <a
            href={
              topProducts.length > 0
                ? `/products/${topProducts[0].product_id}`
                : "#"
            }
            className="hidden text-sm font-semibold text-blue-600 hover:text-blue-500 sm:block"
          >
            Customize your bike
            <span aria-hidden="true"> &rarr;</span>
          </a>
        </div>
        <div className="mt-6 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:grid-rows-2 sm:gap-x-6 lg:gap-8">
          {topProducts.map((product, index) => (
            <div
              className={`group relative aspect-2/1 overflow-hidden rounded-lg sm:aspect-auto ${
                index === 0 ? "sm:row-span-2 sm:aspect-square" : ""
              }`}
            >
              <img
                alt={product.name}
                src={imgPlaceholder[index]}
                className="absolute size-full object-cover group-hover:opacity-75"
              />
              <div
                aria-hidden="true"
                className="absolute inset-0 bg-linear-to-b from-transparent to-black opacity-50"
              />
              <div className="absolute inset-0 flex items-end p-6">
                <div>
                  <h3 className="font-semibold text-white">
                    <a href={`/products/${product.product_id}`}>
                      <span className="absolute inset-0" />
                      {product.name}
                    </a>
                  </h3>
                  <p aria-hidden="true" className="mt-1 text-sm text-white">
                    Shop now
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 sm:hidden">
          <a
            href={`/products/${topProducts[0]}.product_id`}
            className="block text-sm font-semibold text-blue-600 hover:text-blue-500"
          >
            Customize your bike
            <span aria-hidden="true"> &rarr;</span>
          </a>
        </div>
      </div>
    </div>
  );
}
