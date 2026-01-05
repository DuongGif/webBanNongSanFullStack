import React, { useEffect, useState } from "react";
import axios from "axios";

function Category({ onSelectCategory }) {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(""); // Thêm state để lưu loại được chọn

  useEffect(() => {
    axios.get("http://localhost:5000/api/loainongsan/", {
      withCredentials: true // Nếu bạn dùng cookie/session từ backend
    })
      .then(res => {
        if (Array.isArray(res.data)) {
          setCategories(res.data);
        } else {
          console.error("Dữ liệu không hợp lệ:", res.data);
        }
      })
      .catch(err => console.error("Lỗi lấy loại nông sản", err));
  }, []);

  // Hàm xử lý khi chọn loại nông sản
  const handleSelectCategory = (maLoai) => {
    setSelectedCategory(maLoai); // Cập nhật loại được chọn
    onSelectCategory(maLoai); // Gọi callback bên ngoài
  };

  return (
    <div className="category-products panel-group" id="accordian">
      <h2>Loại nông sản</h2>

      {/* Tùy chọn Tất cả */}
      <div className="panel panel-default">
        <div className="panel-heading">
          <h4 className="panel-title">
            <button
              className={`btn btn-link category-button ${selectedCategory === "" ? "selected" : ""}`}
              onClick={() => handleSelectCategory("")}
            >
              Tất cả
            </button>
          </h4>
        </div>
      </div>

      {/* Các loại nông sản */}
      {categories.length === 0 ? (
        <div className="panel panel-default">
          <div className="panel-heading">
            <p>Không có dữ liệu loại nông sản</p>
          </div>
        </div>
      ) : (
        categories.map((loai) => (
          <div className="panel panel-default" key={loai.MaLoai}>
            <div className="panel-heading">
              <h4 className="panel-title">
                <button
                  className={`btn btn-link category-button ${selectedCategory === loai.MaLoai ? "selected" : ""}`}
                  onClick={() => handleSelectCategory(loai.MaLoai)}
                >
                  {loai.TenLoai}
                </button>
              </h4>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Category;
