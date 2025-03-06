import "./Products.css";
import { products } from "../mocks/products.json";
import { useEffect, useState } from "react";
import { fetchProducts } from "../services";
const RelatedProducts = () => {
  const imgPlaceholder = [
    "/assets/mikkel-bech-yjAFnkLtKY0-unsplash (1).jpg",
    "/assets/josh-nuttall-XVTWFHcNIko-unsplash.jpg",
    "/assets/josh-nuttall-zkVi57UYHIQ-unsplash.jpg",
    "/assets/jan-kopriva-dJuCkofVIR8-unsplash.jpg",
  ];

  const [products, setProducts] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const fetchedProducts = await fetchProducts();
      console.log(fetchedProducts);
      setProducts(fetchedProducts);
    }

    fetchData();
  }, []);

  return (
    <section aria-labelledby="related-heading" className="mt-24">
      <h2 id="related-heading" className="text-lg font-medium text-gray-900">
        You may also like&hellip;
      </h2>

      <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
        {products.slice(0, 4).map((relatedProduct, index) => (
          <div key={relatedProduct.id} className="group relative">
            <img
              alt={relatedProduct.name}
              src={imgPlaceholder[index]}
              className="aspect-square w-full rounded-md object-cover group-hover:opacity-75 lg:aspect-auto lg:h-80"
            />
            <div className="mt-4 flex justify-between">
              <div>
                <h3 className="text-sm text-gray-800">
                  <a href={"products/" + relatedProduct.id}>
                    <span aria-hidden="true" className="absolute inset-0" />
                    {relatedProduct.name}
                  </a>
                </h3>
                <p
                  style={{ textTransform: "capitalize" }}
                  className="mt-1 text-sm text-gray-500 "
                >
                  {relatedProduct.category}
                </p>
              </div>
              <p className="text-sm font-medium text-blue-800">Customize now</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RelatedProducts;
