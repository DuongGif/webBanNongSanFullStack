import React, { useState, useEffect, useRef, useContext } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import { UserContext } from '../contexts/UserContext';

const PaymentPage = () => {
  const { user, cartItems } = useContext(UserContext);
  const [paymentUrl, setPaymentUrl] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const amount = searchParams.get('amount') || '0.00';
  const executedRef = useRef(false);

  const createPayment = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/payment/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount,
          MaTaiKhoan: user.maTaiKhoan,
          GioHang: cartItems
        })
      });
      const data = await res.json();
      if (res.ok) {
        setPaymentUrl(data.approval_url);
      } else {
        setError(data.error);
      }
    } catch {
      setError('Lỗi kết nối máy chủ');
    } finally {
      setLoading(false);
    }
  };

  const sendPaymentSuccess = async (paymentId, payerId) => {
    try {
      const res = await fetch('http://localhost:5000/api/payment/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          paymentId,
          PayerID: payerId,
          MaTaiKhoan: user.maTaiKhoan,
          GioHang: cartItems,
          AmountUSD: amount
        })
      });
      const data = await res.json();
      if (res.ok) {
        toast.success('Thanh toán thành công');
        navigate('/payment-success');
      } else {
        toast.error(data.error);
      }
    } catch {
      toast.error('Lỗi kết nối máy chủ');
    }
  };

  useEffect(() => {
    if (!user || !cartItems.length || parseFloat(amount) <= 0) {
      setError('Dữ liệu thanh toán không hợp lệ');
      setLoading(false);
    } else {
      createPayment();
    }

    const handle = (e) => {
      const { status, paymentId, PayerID } = e.data || {};
      if (executedRef.current) return;
      if (status === 'success') {
        executedRef.current = true;
        sendPaymentSuccess(paymentId, PayerID);
      } else if (status === 'cancel') {
        toast.error('Bạn đã hủy thanh toán');
      }
    };

    window.addEventListener('message', handle);
    return () => window.removeEventListener('message', handle);
  }, [user, cartItems, amount, navigate]);

  const openPopup = () => {
    if (paymentUrl) {
      window.open(paymentUrl, 'PayPal', 'width=600,height=700');
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <img
          src="/assets/images/payment/loading.gif"
          alt="Đang xử lý thanh toán"
          style={{ width: '120px', height: '120px', marginBottom: '20px' }}
        />
        <p style={{ fontSize: '18px', color: '#555' }}>
          Đang tạo giao dịch thanh toán, vui lòng chờ...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <p style={{ color: 'red', fontSize: '18px' }}>{error}</p>
      </div>
    );
  }

  return (
    <div style={{ textAlign: 'center', padding: '30px' }}>
      <button
        onClick={openPopup}
        style={{
          backgroundColor: '#0070ba',
          color: 'white',
          fontSize: '18px',
          padding: '12px 24px',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
        }}
      >
        Thanh toán với PayPal
      </button>
    </div>
  );
};

export default PaymentPage;
