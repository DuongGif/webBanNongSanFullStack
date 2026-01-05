// src/components/Cart/CartSummary.js
import React from 'react';

const CartSummary = ({ items, products, shippingFee, onPayment, loading }) => {
  if (!items || !products) return null;

  // Tính tổng tiền sản phẩm
  let subTotal = 0;
  items.forEach(item => {
    const product = products.find(p => p.MaNongSan === item.MaNongSan);
    if (product) {
      subTotal += product.GiaBan * item.SoLuong;
    }
  });

  const total = subTotal + shippingFee;

  return (
    <div className="cart-summary card" style={{ padding: '1.5rem' }}>
      <h4>Tóm tắt đơn hàng</h4>
      <hr />
      <div className="summary-line d-flex justify-content-between">
        <span>Tạm tính:</span>
        <span>{subTotal.toLocaleString()} đ</span>
      </div>
      <div className="summary-line d-flex justify-content-between">
        <span>Phí vận chuyển:</span>
        <span>{shippingFee.toLocaleString()} đ</span>
      </div>
      <hr />
      <div className="summary-line d-flex justify-content-between fw-bold">
        <span>Tổng cộng:</span>
        <span>{total.toLocaleString()} đ</span>
      </div>
      <hr />
      <button
        className="btn btn-success w-100"
        onClick={onPayment}
        disabled={loading}
      >
        {loading ? 'Đang xử lý...' : 'Thanh toán'}
      </button>
    </div>
  );
};

export default CartSummary; // Đây là dòng xuất default
