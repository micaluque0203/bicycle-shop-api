import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import { Home } from "../pages/Home.jsx";
import { ProductPage } from "../pages/ProductPage.jsx";
import { AdminPage } from "../pages/AdminPage.jsx";
import { CartPage } from "../pages/CartPage.jsx";
import Login from "../pages/Login.jsx";
import { Header } from "../components/Header";
import Register from "../pages/Register.jsx";
import { CartProvider } from "../context/cart.jsx";
import { AdminProvider } from "../context/admin.jsx";

function App() {
  return (
    <Router>
      <CartProvider>
        <AdminProvider>
          <Header></Header>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products/:productId" element={<ProductPage />} />
            <Route path="/products" element={<ProductPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </AdminProvider>
      </CartProvider>
    </Router>
  );
}

export default App;
