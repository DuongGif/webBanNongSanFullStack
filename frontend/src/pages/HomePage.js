import React, { useEffect, useState } from "react";
import axios from "axios";
import Category from "../components/Home/Category";
import Brands from "../components/Home/Brands";
import Products from "../components/Products/Products";

function HomePage() { // Chuyển từ NongSanPage -> HomePage
  const [filter, setFilter] = useState({ loai: "", brand: "" });
  const [brandsList, setBrandsList] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/nhacungcap/")
      .then((res) => {
        const formatted = res.data.map(item => ({
          name: item.MaNhaCungCap,
          display: item.TenNhaCungCap,
          count: 0
        }));
        setBrandsList(formatted);
      })
      .catch((err) => console.error("Lỗi lấy danh sách nhà cung cấp", err));
  }, []);

  const handleCategorySelect = (loai) => {
    setFilter((prevFilter) => ({ ...prevFilter, loai }));
  };

  const handleBrandSelect = (brand) => {
    setFilter((prevFilter) => ({ ...prevFilter, brand }));
  };

  return (
    <div className="row">
      <div className="col-sm-3">
        <div className="left-sidebar">
          <Category onSelectCategory={handleCategorySelect} />
          <Brands brands={brandsList} onSelectBrand={handleBrandSelect} />
        </div>
      </div>

      <div className="col-sm-9">
        <Products selectedCategory={filter.loai} selectedBrand={filter.brand} />
      </div>
    </div>
  );
}

export default HomePage; 
