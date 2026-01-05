import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { UserContext } from '../contexts/UserContext';
import QuantityPopup from "../components/Products/QuantityPopup";


function DetailProductPage() {
    const { maNongSan } = useParams();
    const { user, updateCartCount } = useContext(UserContext);
    const [product, setProduct] = useState(null);
    const [supplier, setSupplier] = useState(null);
    const [origin, setOrigin] = useState(null);
    const [loai, setLoai] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [newReview, setNewReview] = useState("");
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [showPopup, setShowPopup] = useState(false);
    const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    if (!maNongSan) return;

    setLoading(true);

    axios.get(`http://localhost:5000/api/nongsan/${maNongSan}`)
      .then((res) => {
        const data = res.data;
        setProduct(data);

        const supplierPromise = axios.get(`http://localhost:5000/api/nhacungcap/${data.MaNhaCungCap}`);
        const originPromise = axios.get(`http://localhost:5000/api/nguongoc/${data.MaNongSan}`);
        const loaiPromise = axios.get(`http://localhost:5000/api/loainongsan/${data.MaLoai}`);

        return Promise.all([supplierPromise, originPromise, loaiPromise]);
      })
      .then(([supplierRes, originRes, loaiRes]) => {
        setSupplier(supplierRes.data);
        setOrigin(originRes.data);
        setLoai(loaiRes.data);
        setLoading(false); // Set loading to false when data is fetched
      })
      .catch((err) => {
        console.error("API error:", err);
        setLoading(false); // Set loading to false on error
      });

    // Lấy danh sách đánh giá cho sản phẩm
    axios.get(`http://localhost:5000/api/review/${maNongSan}`)
      .then((res) => {
        setReviews(res.data);
      })
      .catch((err) => console.error("Error fetching reviews:", err));
  }, [maNongSan]);
  const handleAddToCartClick = () => {
    if (!user) {
      navigate("/login");
      return;
    }
  
    setSelectedProduct(product);
    setShowPopup(true);
  };
  const closePopup = () => setShowPopup(false);
  const handleAddToCartFromPopup = (item) => {
    axios
      .post("http://localhost:5000/api/cart/", {
        MaTaiKhoan: user.maTaiKhoan,
        MaNongSan: item.MaNongSan,
        SoLuong: item.SoLuong,
        GiamGia: item.GiamGia || 0,
        PhiShip: 0,
      })
      .then(() => {
        alert("Đã thêm vào giỏ hàng!");
        updateCartCount();
        closePopup();
      })
      .catch((err) => {
        console.error("Lỗi thêm vào giỏ hàng", err);
        alert("Thêm vào giỏ hàng thất bại.");
      });
  };
    
  const handleReviewSubmit = () => {
    if (newReview.trim() === "") {
      alert("Vui lòng nhập đánh giá.");
      return;
    }

    const user = JSON.parse(localStorage.getItem("user"));
    const maTaiKhoan = user ? user.maTaiKhoan : null;
    if (!maTaiKhoan) {
      alert("Vui lòng đăng nhập trước khi đánh giá.");
      return;
    }

    const reviewData = {
      MaTaiKhoan: maTaiKhoan,
      MaNongSan: maNongSan,
      NoiDung: newReview
    };

    axios.post("http://localhost:5000/api/review/", reviewData)
      .then((res) => {
        console.log("Server response:", res);  // In ra phản hồi của server
        if (res.status === 200) {
          setReviews((prevReviews) => [...prevReviews, res.data]);
          setNewReview("");
          alert("Đánh giá của bạn đã được gửi thành công!");
        } else {
          alert("Có lỗi xảy ra khi gửi đánh giá. Vui lòng thử lại.");
        }
      })
      .catch((err) => {
        console.error("Error posting review:", err);  // Lỗi client-side
        alert("Có lỗi xảy ra khi gửi đánh giá. Vui lòng thử lại.");
      });
  };

  const handleReviewDelete = (reviewId) => {
    const user = JSON.parse(localStorage.getItem("user"));
    const maTaiKhoan = user ? user.maTaiKhoan : null;
  
    if (!maTaiKhoan) {
      alert("Vui lòng đăng nhập để xóa đánh giá.");
      return;
    }
  
    // Kiểm tra xem người dùng có quyền xóa (có phải tài khoản của họ không)
    const reviewToDelete = reviews.find((review) => review.MaReview === reviewId);
  
    if (reviewToDelete && reviewToDelete.MaTaiKhoan !== maTaiKhoan) {
      alert("Bạn không có quyền xóa đánh giá này.");
      return;
    }
  
    axios.delete(`http://localhost:5000/api/review/${reviewId}`)
      .then((res) => {
        if (res.status === 200) {
          setReviews(reviews.filter((review) => review.MaReview !== reviewId));
          alert("Đánh giá đã được xóa.");
        } else {
          alert("Có lỗi xảy ra khi xóa đánh giá. Vui lòng thử lại.");
        }
      })
      .catch((err) => {
        console.error("Error deleting review:", err);
        alert("Có lỗi xảy ra khi xóa đánh giá. Vui lòng thử lại.");
      });
  };
  const handleReviewEdit = (reviewId, currentContent) => {
    const user = JSON.parse(localStorage.getItem("user"));
    const maTaiKhoan = user ? user.maTaiKhoan : null;

    if (!maTaiKhoan) {
      alert("Vui lòng đăng nhập để sửa đánh giá.");
      return;
    }

    // Kiểm tra xem người dùng có quyền sửa (có phải tài khoản của họ không)
    const reviewToEdit = reviews.find((review) => review.MaReview === reviewId);

    if (reviewToEdit && reviewToEdit.MaTaiKhoan !== maTaiKhoan) {
      alert("Bạn không có quyền sửa đánh giá này.");
      return;
    }

    const newContent = prompt("Sửa đánh giá của bạn:", currentContent);
    if (newContent && newContent.trim() !== "") {
      axios.put(`http://localhost:5000/api/review/${reviewId}`, { NoiDung: newContent })
        .then((res) => {
          if (res.status === 200) {
            setReviews(reviews.map((review) =>
              review.MaReview === reviewId ? { ...review, NoiDung: newContent } : review
            ));
            alert("Đánh giá đã được sửa.");
          } else {
            alert("Có lỗi xảy ra khi sửa đánh giá. Vui lòng thử lại.");
          }
        })
        .catch((err) => {
          console.error("Error editing review:", err);
          alert("Có lỗi xảy ra khi sửa đánh giá. Vui lòng thử lại.");
        });
    }
  };

  if (loading) return <p>Đang tải thông tin sản phẩm...</p>;

  return (
    <div className="container">
      <div className="col-sm-9 padding-right">
        <div className="product-details">
          <div className="col-sm-5">
            <div className="view-product">
              <img
                src={`/assets/images/nongsan/${product.DuongDanAnh}`}
                alt={product.TenNongSan}
                className="product-image"
              />
            </div>
          </div>

          <div className="col-sm-7">
            <div className="product-information">
              <h2 className="giant-title">{product.TenNongSan}</h2>
              <p className="big-text">Loại: {loai ? loai.TenLoai : "Đang tải..."}</p>
              <p className="big-text">Khu vực: {origin ? origin.KhuVuc : "Đang tải..."}</p>
              <p className="big-text">Phương pháp: {origin ? origin.PhuongPhap : "Đang tải..."}</p>
              <p className="big-text">
                Số hàng còn lại: {product.SoLuongTonKho} {product.DonViTinh}
              </p>

              <div className="price-qty">
                <span className="price-text">
                  Giá bán: {product.GiaBan} Đồng / {product.DonViTinh}
                </span>
                <label className="big-text">
                  Số lượng:{" "}
                  <input type="number" defaultValue={1} className="small-input" />
                  <button
                        type="button"
                        className="btn btn-default cart"
                        onClick={handleAddToCartClick}
                        >
                        <i className="fa fa-shopping-cart"></i> Add to cart
                        </button>

                </label>
              </div>
            </div>
          </div>
        </div>

        <div className="category-tab shop-details-tab">
          <div className="col-sm-12">
            <ul className="nav nav-tabs">
              <li className="active"><a href="#reviews" data-toggle="tab">Đánh giá</a></li>
              <li><a href="#nhacungcap" data-toggle="tab">Nhà cung cấp</a></li>
            </ul>
          </div>

          <div className="tab-content">
            <div className="tab-pane fade active in" id="reviews">
              <div className="col-sm-12">
                <h4><b>Đánh giá của khách hàng</b></h4>
                {reviews.length > 0 ? (
                  reviews.map((review, index) => (
                  <div key={index} className="review-item">
                    <div className="review-header">
                      <strong>Người đánh giá: </strong>{review.Email}
                      {review.MaTaiKhoan === JSON.parse(localStorage.getItem("user"))?.maTaiKhoan && (
                        <div className="review-actions">
                          <button onClick={() => handleReviewEdit(review.MaReview, review.NoiDung)}>Sửa</button>
                          <button onClick={() => handleReviewDelete(review.MaReview)}>Xóa</button>
                        </div>
                      )}
                    </div>
                    <div className="review-content">
                      <p>{review.NoiDung}</p>
                    </div>
                  </div>
                  ))
                ) : (
                  <p>Chưa có đánh giá nào.</p>
                )}
                <p><b>Viết đánh giá của bạn</b></p>
                <textarea
                  value={newReview}
                  onChange={(e) => setNewReview(e.target.value)}
                  placeholder="Viết đánh giá của bạn..."
                  rows="4"
                  className="form-control"
                />
                <button type="button" className="btn btn-default pull-left" onClick={handleReviewSubmit}>
                  Submit
                </button>
              </div>
            </div>

            <div className="tab-pane fade nhacungcap in" id="nhacungcap">
              {supplier ? (
                <div className="supplier-info" style={{ marginTop: "20px", marginLeft: "20px" }}>
                  <p><strong>Tên nhà cung cấp:</strong> {supplier.TenNhaCungCap}</p>
                  <p><strong>Địa chỉ:</strong> {supplier.DiaChi}</p>
                  <p><strong>SĐT:</strong> {supplier.SoDienThoai}</p>
                </div>
              ) : (
                <p>Đang tải thông tin nhà cung cấp...</p>
              )}
            </div>
          </div>
        </div>
        {showPopup && selectedProduct && (
          <QuantityPopup
            product={selectedProduct}
            onClose={closePopup}
            onAddToCart={handleAddToCartFromPopup}
          />
        )}

      </div>

      <style
        dangerouslySetInnerHTML={{
          __html: `
            .review-item {
              margin-bottom: 15px;
              padding: 10px;
              border: 1px solid #ddd;
              border-radius: 4px;
            }

            .review-header {
              display: flex;
              align-items: center;
              margin-bottom: 10px; /* Khoảng cách giữa header và nội dung */
            }

            .review-actions {
              display: flex;
              gap: 10px;
              margin-left: auto;
            }

            .review-actions button {
              padding: 5px 10px;
              font-size: 14px;
              cursor: pointer;
            }

            .review-content {
              width: 100%;
            }

            .review-content p {
              margin: 0;
              padding: 0;
            }
            .price-text {
              color: #f39c12;
              font-size: 24px;
              font-weight: bold;
            }
            .small-input {
              width: 60px;
              padding: 4px;
              font-size: 14px;
              margin-right: 10px;
              border: 1px solid #ccc;
              border-radius: 4px;
            }
            .product-information .giant-title {
              font-size: 40px;
              margin-bottom: 16px;
              color: #2c3e50;
            }
            .big-title {
              font-size: 30px;
              font-weight: bold;
            }
            .big-text {
              font-size: 18px;
              margin-bottom: 12px;
            }
            .price-qty .big-text {
              display: block;
              margin-bottom: 8px;
            }
          `,
        }}
      />
    </div>
  );
}

export default DetailProductPage;
