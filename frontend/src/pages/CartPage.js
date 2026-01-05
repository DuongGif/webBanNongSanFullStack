import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../contexts/UserContext';
import CartItem from '../components/Cart/CartItem';
import CartSummary from '../components/Cart/CartSummary';
import ShippingFeeCalculator from '../components/Cart/ShippingFeeCalculator';
import { useNavigate } from 'react-router-dom';

function CartPage() {
  const { user } = useContext(UserContext);
  const [cartItems, setCartItems] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [shippingFee, setShippingFee] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    if (!user?.maTaiKhoan) return;

    const fetchCart = async () => {
      setLoading(true);
      try {
        const cartRes = await axios.get(`http://127.0.0.1:5000/api/cart/${user.maTaiKhoan}`);
        setCartItems(cartRes.data);

        const ids = cartRes.data.map(item => item.MaNongSan);
        if (!ids.length) {
          setProducts([]);
          return;
        }

        const productRes = await axios.get(`http://127.0.0.1:5000/api/nongsan/`, {
          params: { ids: ids.join(',') }
        });

        if (productRes.data?.items) {
          setProducts(productRes.data.items);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, [user]);

  const handleUpdateQuantity = (maNongSan, increase) => {
    setLoading(true);
    const updatedCart = cartItems.map(item =>
      String(item.MaNongSan) === String(maNongSan)
        ? { ...item, SoLuong: Math.max(item.SoLuong + (increase ? 1 : -1), 1) }
        : item
    );
    setCartItems(updatedCart);

    axios.put(`http://127.0.0.1:5000/api/cart/${user.maTaiKhoan}/${maNongSan}`, {
      SoLuong: updatedCart.find(item => String(item.MaNongSan) === String(maNongSan)).SoLuong
    })
      .catch(err => {
        console.error('Cập nhật số lượng thất bại', err);
        alert('Có lỗi xảy ra khi cập nhật số lượng sản phẩm.');
      })
      .finally(() => setLoading(false));
  };

  const handleRemove = (maNongSan) => {
    setLoading(true);
    axios.delete(`http://127.0.0.1:5000/api/cart/${user.maTaiKhoan}/${maNongSan}`)
      .then(() => {
        setCartItems(ci => ci.filter(i => String(i.MaNongSan) !== String(maNongSan)));
      })
      .catch(err => {
        console.error('Xóa thất bại', err);
        alert('Có lỗi xảy ra khi xóa sản phẩm.');
      })
      .finally(() => setLoading(false));
  };

  const handlePayment = () => {
    if (!products.length) {
      alert("Không có sản phẩm hợp lệ để thanh toán.");
      return;
    }

    const totalVND = cartItems.reduce((sum, item) => {
      const p = products.find(x => String(x.MaNongSan) === String(item.MaNongSan));
      if (!p) return sum;
      const discounted = p.GiaBan * (1 - (item.GiamGia || 0) / 100);
      return sum + discounted * item.SoLuong;
    }, 0) + shippingFee;

    if (totalVND <= 0) {
      alert("Tổng tiền không hợp lệ.");
      return;
    }

    navigate(`/payment?amount=${totalVND}`);
  };

  const handleShippingFeeSelected = (fee) => {
    setShippingFee(fee);
  };

  if (!user) return <p>Vui lòng đăng nhập để xem giỏ hàng.</p>;

  return (
    <div className="cart-page-container" style={{ padding: '2rem' }}>
      <section id="cart_items">
        <div className="container">
          <div className="breadcrumbs">
            <ol className="breadcrumb">
              <li><a href="/">Home</a></li>
              <li className="active">Shopping Cart</li>
            </ol>
          </div>
          <div className="table-responsive cart_info">
            <table className="table table-condensed">
              <thead>
                <tr className="cart_menu">
                  <td className="image">Item</td>
                  <td className="description">Description</td>
                  <td className="price">Price</td>
                  <td className="quantity">Quantity</td>
                  <td className="total">Total</td>
                  <td></td>
                </tr>
              </thead>
              <tbody>
                {cartItems.length === 0 ? (
                  <tr>
                    <td colSpan="6">Giỏ hàng của bạn hiện tại không có sản phẩm nào.</td>
                  </tr>
                ) : (
                  cartItems.map(item => {
                    const product = products.find(p => String(p.MaNongSan) === String(item.MaNongSan));
                    if (!product) {
                      return (
                        <tr key={item.MaNongSan}>
                          <td colSpan="6">Không tìm thấy sản phẩm này trong kho.</td>
                        </tr>
                      );
                    }
                    return (
                      <CartItem
                        key={item.MaNongSan}
                        product={product}
                        item={item}
                        onRemove={() => handleRemove(item.MaNongSan)}
                        onIncreaseQuantity={() => handleUpdateQuantity(item.MaNongSan, true)}
                        onDecreaseQuantity={() => handleUpdateQuantity(item.MaNongSan, false)}
                      />
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section id="cart_summary">
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <ShippingFeeCalculator onShippingFeeSelected={handleShippingFeeSelected} />
            </div>
            <div className="col-md-6">
              <CartSummary
                items={cartItems}
                products={products}
                shippingFee={shippingFee}
                onPayment={handlePayment}
                loading={loading}
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default CartPage;
