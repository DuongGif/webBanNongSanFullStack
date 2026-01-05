import React, { useEffect, useState, useContext } from "react";
import { UserContext } from "../../contexts/UserContext";
import axios from "axios";

function Information() {
  const { user, setUser } = useContext(UserContext); // nếu muốn cập nhật userContext sau khi lưu
  const [accountInfo, setAccountInfo] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    HoTen: "",
    DiaChi: "",
    SoDienThoai: "",
  });

  useEffect(() => {
    if (user?.maTaiKhoan) {
      axios
        .get(`http://127.0.0.1:5000/api/taikhoan/${user.maTaiKhoan}`)
        .then((res) => {
          setAccountInfo(res.data);
          setFormData({
            HoTen: res.data.HoTen || "",
            DiaChi: res.data.DiaChi || "",
            SoDienThoai: res.data.SoDienThoai || "",
          });
        })
        .catch((err) => {
          console.error("Lỗi khi lấy thông tin tài khoản", err);
        });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    const updatedData = {
      ...accountInfo,
      HoTen: formData.HoTen,
      DiaChi: formData.DiaChi,
      SoDienThoai: formData.SoDienThoai,
    };

    axios
      .put(`http://127.0.0.1:5000/api/taikhoan/${user.maTaiKhoan}`, updatedData)
      .then((res) => {
        setAccountInfo(res.data); // cập nhật lại thông tin mới ngay
        setFormData({
          HoTen: res.data.HoTen || "",
          DiaChi: res.data.DiaChi || "",
          SoDienThoai: res.data.SoDienThoai || "",
        });
        setIsEditing(false);

        // (Tùy chọn) nếu bạn muốn cập nhật lại UserContext
        if (setUser) {
          setUser((prev) => ({
            ...prev,
            HoTen: res.data.HoTen,
            DiaChi: res.data.DiaChi,
            SoDienThoai: res.data.SoDienThoai,
          }));
        }
      })
      .catch((err) => {
        console.error("Lỗi khi cập nhật thông tin", err);
      });
  };

  if (!accountInfo) {
    return <div>Đang tải thông tin...</div>;
  }

  return (
    <div className="information-container">
      <h2>Thông tin tài khoản</h2>

      <div className="info-item">
        <strong>Họ tên:</strong>{" "}
        {isEditing ? (
          <input
            type="text"
            name="HoTen"
            value={formData.HoTen}
            onChange={handleChange}
          />
        ) : (
          <span>{accountInfo.HoTen || "Chưa có họ tên"}</span>
        )}
      </div>

      <div className="info-item">
        <strong>Địa chỉ:</strong>{" "}
        {isEditing ? (
          <input
            type="text"
            name="DiaChi"
            value={formData.DiaChi}
            onChange={handleChange}
          />
        ) : (
          <span>{accountInfo.DiaChi || "Chưa có địa chỉ"}</span>
        )}
      </div>

      <div className="info-item">
        <strong>Số điện thoại:</strong>{" "}
        {isEditing ? (
          <input
            type="text"
            name="SoDienThoai"
            value={formData.SoDienThoai}
            onChange={handleChange}
          />
        ) : (
          <span>{accountInfo.SoDienThoai || "Chưa có số điện thoại"}</span>
        )}
      </div>

      <div className="info-item">
        <strong>Email:</strong>{" "}
        <span>{accountInfo.Email || "Chưa có email"}</span>
      </div>

      <div className="info-item">
        <strong>Loại tài khoản:</strong>{" "}
        <span>{accountInfo.LoaiTaiKhoan}</span>
      </div>

      <div className="info-actions" style={{ marginTop: "20px" }}>
        {isEditing ? (
          <>
            <button onClick={handleSave}>Lưu</button>
            <button
              onClick={() => {
                // Hủy chỉnh sửa, khôi phục dữ liệu gốc
                setFormData({
                  HoTen: accountInfo.HoTen || "",
                  DiaChi: accountInfo.DiaChi || "",
                  SoDienThoai: accountInfo.SoDienThoai || "",
                });
                setIsEditing(false);
              }}
              style={{ marginLeft: "10px" }}
            >
              Hủy
            </button>
          </>
        ) : (
          <button onClick={() => setIsEditing(true)}>Sửa</button>
        )}
      </div>
    </div>
  );
}

export default Information;
