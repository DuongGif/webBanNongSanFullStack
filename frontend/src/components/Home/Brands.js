import React, { useEffect, useState } from "react";
import axios from "axios";

function Brands({ onSelectBrand, selectedBrand }) {
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/nhacungcap/")
      .then((res) => setBrands(res.data))
      .catch((err) => console.error("Lỗi lấy danh sách nhà cung cấp", err));
  }, []);

  return (
    <div className="brands_products">
      <h2 className="text-lg font-bold mb-2 text-orange-500 uppercase border-b pb-1 mb-3">Nhà cung cấp</h2>
      <div className="brands-name">
        <ul className="space-y-10"> {/* Tăng khoảng cách giữa các dòng tại đây */}

          {/* Tùy chọn tất cả */}
          <li>
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                onSelectBrand("");
              }}
              className={`block px-3 py-1 rounded transition-colors duration-200 ${
                selectedBrand === ""
                  ? "text-red-600 font-semibold underline bg-red-50"
                  : "text-blue-600 hover:underline"
              }`}
            >
              Tất cả
            </a>
          </li>

          {/* Danh sách các nhà cung cấp */}
          {brands.map((item) => (
            <li key={item.MaNhaCungCap}>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  onSelectBrand(item.MaNhaCungCap);
                }}
                className={`block px-3 py-1 rounded transition-colors duration-200 ${
                  selectedBrand === item.MaNhaCungCap
                    ? "text-red-600 font-semibold underline bg-red-50"
                    : "text-blue-600 hover:underline"
                }`}
              >
                {item.TenNhaCungCap}
              </a>
            </li>
          ))}

        </ul>
      </div>
    </div>
  );
}

export default Brands;
