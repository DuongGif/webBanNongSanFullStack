import React, { useState, useContext } from "react";
import axios from "axios";
import Login from "../components/Login/Login";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../contexts/UserContext";

function LoginPage() {
  const [loginData, setLoginData] = useState({ email: "", password: "" });
  const [signupData, setSignupData] = useState({ name: "", email: "", password: "", otp: "" });
  const [otpSent, setOtpSent] = useState(false);
  const [otpError, setOtpError] = useState("");

  const navigate = useNavigate();
  const { setUser } = useContext(UserContext);

  const handleLoginChange = (e) => {
    setLoginData({ ...loginData, [e.target.name]: e.target.value });
  };

  const handleSignupChange = (e) => {
    setSignupData({ ...signupData, [e.target.name]: e.target.value });
  };

  const handleSendOtp = async () => {
    if (!signupData.email) {
      alert("Vui lòng nhập email.");
      return;
    }

    try {
      await axios.post("http://localhost:5000/api/otp/sendotp", {
        email: signupData.email,
      });
      alert("Mã OTP đã được gửi đến email của bạn.");
      setOtpSent(true);
    } catch (err) {
      console.error(err);
      setOtpError("Gửi OTP thất bại: " + (err.response?.data?.error || "Có lỗi xảy ra"));
    }
  };

  const verifyOtp = async () => {
    try {
      const res = await axios.post("http://localhost:5000/api/otp/verifyotp", {
        email: signupData.email,
        otp_received: signupData.otp,
      });
      return res.data.message === "OTP verified successfully!";
    } catch (err) {
      alert("Xác thực OTP thất bại: " + (err.response?.data?.error || "Có lỗi xảy ra"));
      return false;
    }
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    if (!loginData.email || !loginData.password) {
      alert("Vui lòng nhập email và mật khẩu.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/api/taikhoan/login", {
        email: loginData.email,
        password: loginData.password,
      });

      if (res.data && res.data.MaTaiKhoan) {
        const userData = {
          maTaiKhoan: res.data.MaTaiKhoan,
          email: loginData.email,
          role: res.data.LoaiTaiKhoan, // Thêm vai trò (Admin hoặc Khach)
        };

        alert("Đăng nhập thành công!");
        setUser(userData);
        localStorage.setItem("user", JSON.stringify(userData));

        if (userData.role === "Admin") {
          navigate("/admin"); // Điều hướng tới trang admin nếu là Admin
        } else {
          navigate("/"); // Điều hướng tới trang chủ nếu là Khach
        }
      } else {
        alert("Đăng nhập thất bại: Không tìm thấy tài khoản.");
      }
    } catch (err) {
      console.error(err.response);
      alert("Đăng nhập thất bại: " + (err.response?.data?.error || "Có lỗi xảy ra"));
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();

    const otpValid = await verifyOtp();
    if (!otpValid) return;

    try {
      const getRes = await axios.get("http://localhost:5000/api/taikhoan");
      const accounts = getRes.data;

      const nextIndex = accounts.length + 1;
      let maTaiKhoan = "TK" + nextIndex.toString().padStart(2, "0");
      const accountExists = accounts.some((account) => account.MaTaiKhoan === maTaiKhoan);
      if (accountExists) {
        maTaiKhoan = "TK" + (accounts.length + 2).toString().padStart(2, "0");
      }

      const res = await axios.post("http://localhost:5000/api/taikhoan/signup", {
        MaTaiKhoan: maTaiKhoan,
        MatKhau: signupData.password,
        LoaiTaiKhoan: "Khach",
        HoTen: signupData.name,
        DiaChi: "",
        SoDienThoai: "",
        Email: signupData.email,
      });

      const userData = {
        maTaiKhoan: maTaiKhoan,
        email: signupData.email,
        role: "Khach",
      };

      alert("Đăng ký thành công!");
      setUser(userData);
      localStorage.setItem("user", JSON.stringify(userData));
      setSignupData({ name: "", email: "", password: "", otp: "" });

      navigate("/");
    } catch (err) {
      console.error(err);
      alert("Lỗi khi đăng ký: " + (err.response?.data?.error || "Có lỗi xảy ra"));
    }
  };

  const handleGoHome = () => {
    navigate("/");
  };

  return (
    <div>
      <Login
        loginData={loginData}
        handleLoginChange={handleLoginChange}
        handleLoginSubmit={handleLoginSubmit}
        signupData={signupData}
        handleSignupChange={handleSignupChange}
        handleSendOtp={handleSendOtp}
        handleSignupSubmit={handleSignupSubmit}
        otpSent={otpSent}
        otpError={otpError}
        handleGoHome={handleGoHome}
      />
    </div>
  );
}

export default LoginPage;
