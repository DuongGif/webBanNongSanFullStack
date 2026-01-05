import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function PaymentSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      // Điều hướng về trang chủ
      navigate("/");

      // Reload toàn bộ trang sau khi chuyển hướng
      window.location.reload();
    }, 3000); // Chuyển về homepage sau 3 giây

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h2 style={{ color: "green", fontSize: "28px", marginBottom: "20px" }}>
        ✅ Thanh toán thành công!
      </h2>
      <img
        src="/assets/images/payment/thanhcong.gif"
        alt="Thanh toán thành công"
        style={{ width: "300px", maxWidth: "90%", marginBottom: "20px" }}
      />
      <p style={{ fontSize: "18px" }}>
        Bạn sẽ được chuyển về trang chủ trong giây lát...
      </p>
    </div>
  );
}

export default PaymentSuccess;
