import React, { useMemo, useContext } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
  matchPath,
  Navigate,
} from "react-router-dom";
import HomePage from "./pages/HomePage";
import PaymentPage from "./pages/PaymentPage";
import PaymentSuccess from "./pages/PaymentSuccess";
import PaymentCancel from "./pages/PaymentCancel";
import Header from "./components/Home/Header";
import Footer from "./components/Home/Footer";
import Slide from "./components/Home/Slide";
import LoginPage from "./pages/LoginPage";
import CartPage from "./pages/CartPage";
import AccountPage from "./pages/AccountPage";
import AdminPage from "./pages/AdminPage";
import AddProductForm from "./components/Admin/AddProductForm";
import DeleteProductForm from "./components/Admin/DeleteProductForm";
import EditProductForm from "./components/Admin/EditProductForm";
import DetailProductPage from "./pages/DetailProductPage"; 
import ContactPage from "./pages/ContactPage"; 

import { UserProvider, UserContext } from "./contexts/UserContext";

// Component bảo vệ các route Admin
function AdminRoute({ element }) {
  const { user } = useContext(UserContext);

  if (!user || user.role !== "Admin") {
    return <Navigate to="/" replace />;
  }

  return element;
}

// Component bảo vệ các route người dùng
function UserRoute({ element }) {
  const { user } = useContext(UserContext);

  if (user && user.role === "Admin") {
    return <Navigate to="/admin" replace />;
  }

  return element;
}

function AppContent() {
  const location = useLocation();

  // Các route cần ẩn các thành phần
  const hideHeaderFooterPaths = ["/payment", "/payment-success", "/payment-cancel", "/login", "/admin"];
  const hideSlidePaths = [...hideHeaderFooterPaths, "/cart", "/account","/:maNongSan","/contact"];

  const shouldHideHeaderFooter = useMemo(
    () => hideHeaderFooterPaths.some((path) =>
      matchPath({ path, end: false }, location.pathname)
    ),
    [location.pathname]
  );

  const shouldHideSlide = useMemo(
    () => hideSlidePaths.some((path) =>
      matchPath({ path, end: false }, location.pathname)
    ),
    [location.pathname]
  );

  return (
    <>
      {!shouldHideHeaderFooter && <Header />}
      {!shouldHideSlide && <Slide />}

      <Routes>
        {/* Các route người dùng */}
        <Route path="/" element={<UserRoute element={<HomePage />} />} />
        <Route path="/cart" element={<UserRoute element={<CartPage />} />} />
        <Route path="/account" element={<UserRoute element={<AccountPage />} />} />
        <Route path="/product/:id" element={<UserRoute element={<HomePage />} />} />
        <Route path="/:maNongSan" element={<DetailProductPage />} /> 
 
        {/* Các route không cần kiểm tra quyền */}  
        <Route path="/payment" element={<PaymentPage />} />
        <Route path="/payment-success" element={<PaymentSuccess />} />
        <Route path="/payment-cancel" element={<PaymentCancel />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/contact" element={<ContactPage />} />

        {/* Các route Admin */}
        <Route path="/admin" element={<AdminRoute element={<AdminPage />} />} />
        <Route
          path="/admin/:section/add"
          element={<AdminRoute element={<AddProductForm />} />}
        />
        <Route
          path="/admin/:section/edit/:id"
          element={<AdminRoute element={<EditProductForm />} />}
        />
        <Route
          path="/admin/delete/:section"
          element={<AdminRoute element={<DeleteProductForm />} />}
        />
      </Routes>

      {!shouldHideHeaderFooter && <Footer />}
    </>
  );
}

function App() {
  return (
    <UserProvider>
      <Router>
        <AppContent />
      </Router>
    </UserProvider>
  );
}

export default App;
