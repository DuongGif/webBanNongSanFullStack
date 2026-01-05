import React from "react";
import Information from "../components/Login/Information";
import OrderHistory from "../components/Cart/OrderHistory"; // 👈 Chỉnh lại đường dẫn import

function AccountPage() {
  return (
    <div className="information-page">
      <h1>Trang Thông Tin Tài Khoản</h1>
      <Information />

      <hr style={{ margin: "40px 0" }} /> {/* Ngăn cách đẹp giữa các phần */}

      <OrderHistory /> {/* Hiển thị lịch sử đơn hàng */}
    </div>
  );
}

export default AccountPage;
