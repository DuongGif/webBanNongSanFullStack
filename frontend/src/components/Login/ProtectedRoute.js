import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { UserContext } from "../contexts/UserContext";

function ProtectedRoute({ children, roleRequired }) {
  const { user } = useContext(UserContext);

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (roleRequired && user.role !== roleRequired) {
    return <Navigate to="/" />; // Điều hướng về trang chủ nếu vai trò không khớp
  }

  return children;
}

export default ProtectedRoute;
