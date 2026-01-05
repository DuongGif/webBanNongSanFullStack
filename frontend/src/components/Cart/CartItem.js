import React, { useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../../contexts/UserContext';

const CartItem = ({ product, item, onRemove, onIncreaseQuantity, onDecreaseQuantity }) => {
  const { user } = useContext(UserContext);
  if (!product || !item || !user) return null;

  const discountPrice = product.GiaBan * (1 - (item.GiamGia || 0) / 100);
  const total = discountPrice * item.SoLuong + item.PhiShip;

  // Unified function to update quantity on backend and trigger correct callback
  const updateQuantity = (newQuantity, isIncrease) => {
    axios.put(
      `http://127.0.0.1:5000/api/cart/${user.maTaiKhoan}/${item.MaNongSan}`,
      { SoLuong: newQuantity, GiamGia: item.GiamGia, PhiShip: item.PhiShip }
    )
    .then(response => {
      console.log(response.data);
      if (isIncrease) {
        onIncreaseQuantity(item.MaNongSan, newQuantity);
      } else {
        onDecreaseQuantity(item.MaNongSan, newQuantity);
      }
    })
    .catch(error => {
      console.error('Cập nhật số lượng thất bại', error);
      // Optionally show user feedback here
    });
  };

  // Handlers
  const handleIncrease = () => updateQuantity(item.SoLuong + 1, true);
  const handleDecrease = () => {
    if (item.SoLuong > 1) {
      updateQuantity(item.SoLuong - 1, false);
    }
  };

  return (
    <tr>
      <td className="cart_product">
        <img src={`/assets/images/nongsan/${product.DuongDanAnh}`} alt={product.TenNongSan} />
      </td>
      <td className="cart_description">
        <h4>{product.TenNongSan}</h4>
        <p>Web ID: {product.MaNongSan}</p>
      </td>
      <td className="cart_price">
        <p>{product.GiaBan.toLocaleString()} đ</p>
      </td>
      <td className="cart_quantity">
        <div className="cart_quantity_button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button className="cart_quantity_down" onClick={handleDecrease} disabled={item.SoLuong <= 1}>
            –
          </button>
          <input
            className="cart_quantity_input"
            type="text"
            value={item.SoLuong}
            readOnly
            size="2"
            autoComplete="off"
            style={{ textAlign: 'center', width: '40px' }}
          />
          <button className="cart_quantity_up" onClick={handleIncrease}>
            +
          </button>
        </div>
      </td>
      <td className="cart_total">
        <p className="cart_total_price">{total.toLocaleString()} đ</p>
      </td>
      <td className="cart_delete">
        <button className="cart_quantity_delete" onClick={() => onRemove(item.MaNongSan)}>
          <i className="fa fa-times" />
        </button>
      </td>
    </tr>
  );
};

export default CartItem;
