import React, { createContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const stored = JSON.parse(localStorage.getItem('user') || 'null');
  const [user, setUser] = useState(stored);
  const [cartItems, setCartItems] = useState([]);

  // Cập nhật giỏ hàng từ server
  const updateCartCount = useCallback(async () => {
    if (!user?.maTaiKhoan) {
      setCartItems([]);
      return;
    }

    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/api/cart/${user.maTaiKhoan}`
      );

      if (Array.isArray(res.data)) {
        setCartItems(res.data);
      } else {
        console.error('Dữ liệu không hợp lệ từ API:', res.data);
        setCartItems([]);
      }
    } catch (error) {
      console.error('Lỗi cập nhật giỏ hàng:', error);
    }
  }, [user]);

  useEffect(() => {
    updateCartCount();
  }, [user, updateCartCount]);

  const addToCart = async (newItem) => {
    setCartItems((prev) => {
      const idx = prev.findIndex((i) => i.MaNongSan === newItem.MaNongSan);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = {
          ...copy[idx],
          SoLuong: copy[idx].SoLuong + (newItem.SoLuong || 1),
        };
        return copy;
      }
      return [...prev, { ...newItem, SoLuong: newItem.SoLuong || 1 }];
    });

    if (user) {
      try {
        await axios.post('http://127.0.0.1:5000/api/cart/', {
          MaTaiKhoan: user.maTaiKhoan,
          MaNongSan: newItem.MaNongSan,
          SoLuong: newItem.SoLuong || 1,
          GiamGia: newItem.GiamGia || 0,
          PhiShip: 0,
        });
      } catch (error) {
        console.error('Lỗi khi thêm vào giỏ hàng trên server', error);
      }
    }
  };

  const removeFromCart = async (itemId) => {
    setCartItems((prev) => prev.filter((item) => item.MaNongSan !== itemId));

    if (user) {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/cart/${user.maTaiKhoan}/${itemId}`);
      } catch (error) {
        console.error('Lỗi khi xóa sản phẩm khỏi giỏ hàng trên server', error);
      }
    }
  };

  const clearCart = async () => {
    setCartItems([]);

    if (user) {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/cart/clear/${user.maTaiKhoan}`);
      } catch (error) {
        console.error('Lỗi khi xoá toàn bộ giỏ hàng trên server:', error);
      }
    }
  };

  const getCartCount = () =>
    cartItems.reduce((sum, item) => sum + (item.SoLuong || 0), 0);

  return (
    <UserContext.Provider
      value={{
        user,
        setUser,
        cartItems,
        addToCart,
        removeFromCart,
        getCartCount,
        updateCartCount,
        clearCart,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
