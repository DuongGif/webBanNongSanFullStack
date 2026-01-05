import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from '../../contexts/UserContext';
import { useNavigate } from "react-router-dom";
import QuantityPopup from './QuantityPopup'; // Import popup component

function Products({ selectedCategory, selectedBrand }) {
  const { user, updateCartCount } = useContext(UserContext);
  const navigate = useNavigate();

  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(1);
  const [limit] = useState(6);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  // Fetch products (with filters, pagination, and search)
  useEffect(() => {
    setLoading(true);
    const params = { page, limit };
    if (selectedCategory) params.category = selectedCategory;
    if (selectedBrand) params.brand = selectedBrand;
    if (searchTerm.trim() !== "") params.search = searchTerm;

    axios.get("http://localhost:5000/api/nongsan/", { params })
      .then(res => {
        // Backend returns { items: [...], pagination: {...} }
        setProducts(res.data.items || []);
        setTotalPages(res.data.pagination?.pages || 1);
      })
      .catch(err => {
        console.error("Lỗi lấy danh sách nông sản", err);
        setProducts([]);
      })
      .finally(() => setLoading(false));
  }, [page, limit, selectedCategory, selectedBrand, searchTerm]);

  // Reset to first page when filters or search change
  useEffect(() => {
    setPage(1);
  }, [selectedCategory, selectedBrand, searchTerm]);

  const handleAddToCart = (item) => {
    if (!user) {
      navigate("/login");
      return;
    }
    setSelectedProduct(item);
    setShowPopup(true);
  };

  const handleClickProduct = (maNongSan) => {
    navigate(`/${maNongSan}`);
  };

  const closePopup = () => setShowPopup(false);

  const handleAddToCartFromPopup = (item) => {
    axios.post("http://localhost:5000/api/cart/", {
      MaTaiKhoan: user.maTaiKhoan,
      MaNongSan: item.MaNongSan,
      SoLuong: item.SoLuong,
      GiamGia: item.GiamGia || 0,
      PhiShip: 0
    })
    .then(() => {
      alert("Đã thêm vào giỏ hàng!");
      updateCartCount();
    })
    .catch(err => {
      console.error("Lỗi thêm vào giỏ hàng", err);
      alert("Thêm vào giỏ hàng thất bại.");
    });
  };

  const handlePrev = () => page > 1 && setPage(page - 1);
  const handleNext = () => page < totalPages && setPage(page + 1);

  const renderPagination = () => {
    const pagesToShow = 5;
    const start = Math.max(1, page - Math.floor(pagesToShow / 2));
    const end = Math.min(totalPages, start + pagesToShow - 1);
    const actualStart = Math.max(1, end - pagesToShow + 1);
    const pageNumbers = [];
    for (let p = actualStart; p <= end; p++) pageNumbers.push(p);

    return (
      <div className="pagination">
        <button onClick={handlePrev} disabled={page === 1} className="btn btn-sm btn-light">« Trước</button>
        {pageNumbers.map(p => (
          <button
            key={p}
            onClick={() => setPage(p)}
            className={`btn btn-sm ${p === page ? "btn-primary" : "btn-light"} mx-1`}
          >
            {p}
          </button>
        ))}
        <button onClick={handleNext} disabled={page === totalPages} className="btn btn-sm btn-light">Tiếp »</button>
      </div>
    );
  };

  return (
    <div className="col-sm-12 padding-right">
      <div className="header-bottom">
        
          <div className="row">
            <div className="col-sm-1"></div>
            <div className="col-sm-11">
            <div className="search_box pull-right">
              <input
                type="text"
                className="search-input" // Thêm class để điều chỉnh CSS
                placeholder="Tìm kiếm sản phẩm..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />

            </div>
          </div>
        </div>
      </div>

      <h2 className="title text-center">Danh sách Nông sản</h2>

      {loading ? (
        <div className="text-center">Đang tải...</div>
      ) : products.length > 0 ? (
        <div className="features_items row">
          {products.map(item => (
            <div className="col-sm-4" key={item.MaNongSan}>
              <div className="product-image-wrapper">
                <div className="single-products">
                  <div className="productinfo text-center">
                    <img
                      src={`/assets/images/nongsan/${item.DuongDanAnh}`}
                      alt={item.TenNongSan}
                      style={{ width: "100%", height: "200px", objectFit: "cover", cursor: "pointer" }}
                      onClick={() => handleClickProduct(item.MaNongSan)}
                    />
                    <h2>{item.GiaBan?.toLocaleString()} đ</h2>
                    <p>{item.TenNongSan}</p>
                    <button
                      className="btn btn-default add-to-cart"
                      onClick={() => handleAddToCart(item)}
                    >
                      <i className="fa fa-shopping-cart"></i> Thêm vào giỏ
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>Không có sản phẩm nào.</p>
      )}

      <div className="text-center mt-3">
        {renderPagination()}
      </div>

      {showPopup && selectedProduct && (
        <QuantityPopup
          product={selectedProduct}
          onClose={closePopup}
          onAddToCart={handleAddToCartFromPopup}
        />
      )}
    </div>
  );
}

export default Products;
