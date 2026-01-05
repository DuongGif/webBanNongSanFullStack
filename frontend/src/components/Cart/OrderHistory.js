import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { UserContext } from "../../contexts/UserContext";

function OrderHistory() {
  const { user } = useContext(UserContext); // Lấy thông tin người dùng từ UserContext
  const [orders, setOrders] = useState([]); // Lưu danh sách đơn hàng
  const [loading, setLoading] = useState(true); // Trạng thái tải dữ liệu
  const [error, setError] = useState(null); // Lưu thông tin lỗi nếu có

  useEffect(() => {
    // Chỉ thực hiện nếu tài khoản người dùng tồn tại
    if (user?.maTaiKhoan) {
      setLoading(true);
      setError(null);

      axios
        .get(`http://127.0.0.1:5000/api/hoadon/${user.maTaiKhoan}`)
        .then((res) => {
          setOrders(res.data);
          setLoading(false);
        })
        .catch((err) => {
          setError("Không thể tải danh sách đơn hàng. Vui lòng thử lại.");
          setLoading(false);
        });
    }
  }, [user]);

  const handleCancelOrder = (maHoaDon) => {
    if (window.confirm("Bạn có chắc chắn muốn hủy đơn hàng này?")) {
      axios
        .delete(`http://127.0.0.1:5000/api/hoadon/${maHoaDon}`)
        .then(() => {
          setOrders((prevOrders) =>
            prevOrders.filter((order) => order.MaHoaDon !== maHoaDon)
          );
          alert("Đơn hàng đã được hủy thành công.");
        })
        .catch(() => {
          alert("Không thể hủy đơn hàng. Vui lòng thử lại.");
        });
    }
  };

  const handleEditOrder = (maHoaDon) => {
    // Chuyển hướng đến trang chỉnh sửa đơn hàng
    alert(`Chuyển hướng đến trang chỉnh sửa đơn hàng: ${maHoaDon}`);
    // Ví dụ: `window.location.href = /edit-order/${maHoaDon}`;
  };

  if (!user?.maTaiKhoan) {
    return <p>Bạn cần đăng nhập để xem lịch sử đơn hàng.</p>;
  }

  if (loading) {
    return <p>Đang tải danh sách đơn hàng...</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  return (
    <div className="order-history">
      <h2>Lịch sử đơn hàng</h2>
      {orders.length === 0 ? (
        <p>Bạn chưa có đơn hàng nào.</p>
      ) : (
        orders.map((order) => (
          <div key={order.MaHoaDon} className="order-card">
            <h3 style={{ color: "red" }}>Đơn hàng #{order.MaHoaDon}</h3>
            <p>
              <strong>Ngày xuất:</strong> {order.NgayXuat || "Chưa xác định"}
            </p>
            <p>
              <strong>Tổng tiền:</strong>{" "}
              {order.TongTien ? order.TongTien.toLocaleString() : "0"} VND
            </p>
            <div className="order-details">
              <h4>Chi tiết đơn hàng:</h4>
              {order.ChiTiet && order.ChiTiet.length === 0 ? (
                <p>Không có chi tiết cho đơn hàng này.</p>
              ) : (
                <table className="order-details-table">
                  <thead>
                    <tr>
                      <th>Tên nông sản</th>
                      <th>Số lượng</th>
                      <th>Đơn giá</th>
                      <th>Giảm giá</th>
                    </tr>
                  </thead>
                  <tbody>
                    {order.ChiTiet?.map((item, index) => (
                      <tr key={index}>
                        <td>{item.TenNongSan || "N/A"}</td>
                        <td>{item.SoLuong || "0"}</td>
                        <td>
                          {item.DonGia
                            ? item.DonGia.toLocaleString()
                            : "0"}{" "}
                          VND
                        </td>
                        <td>{item.GiamGia ? `${item.GiamGia}%` : "0%"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
            <div className="order-actions">
              <button
                onClick={() => handleCancelOrder(order.MaHoaDon)}
                className="cancel-order-button"
              >
                Hủy đơn hàng
              </button>
              <button
                onClick={() => handleEditOrder(order.MaHoaDon)}
                className="edit-order-button"
              >
                Chỉnh sửa đơn hàng
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default OrderHistory;
