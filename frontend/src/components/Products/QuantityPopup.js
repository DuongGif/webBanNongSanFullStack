import React, { useState } from "react";

function QuantityPopup({ product, onClose, onAddToCart }) {
  const [quantity, setQuantity] = useState(1);

  const handleAddToCart = () => {
    onAddToCart({ ...product, SoLuong: quantity });
    onClose(); 
  };

  return (
    <div className="popup-overlay">
      <div className="popup-container">
        <div className="popup-header">
          <h3>Chỉnh sửa số lượng</h3>
          <button className="close-btn" onClick={onClose}>X</button>
        </div>
        <div className="popup-body">
          <p>{product.TenNongSan}</p>
          <img
            src={`/assets/images/nongsan/${product.DuongDanAnh}`}
            alt={product.TenNongSan}
            style={{ width: "100px", height: "100px", objectFit: "cover" }}
          />
          <h2>{product.GiaBan.toLocaleString()} đ</h2>
          <label>Số lượng:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Math.max(1, e.target.value))}
            min="1"
          />
        </div>
        <div className="popup-footer">
          <button className="btn btn-primary" onClick={handleAddToCart}>Thêm vào giỏ hàng</button>
        </div>
      </div>
    </div>
  );
}

export default QuantityPopup;
