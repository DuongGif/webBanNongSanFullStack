import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/button';
import { Input } from '../ui/input';

const sectionsData = {
  loainongsan: [
    { name: 'MaLoai', label: 'Mã Loại', type: 'text' },
    { name: 'TenLoai', label: 'Tên Loại', type: 'text' },
  ],
  nhacungcap: [
    { name: 'MaNhaCungCap', label: 'Mã Nhà Cung Cấp', type: 'text' },
    { name: 'TenNhaCungCap', label: 'Tên Nhà Cung Cấp', type: 'text' },
    { name: 'DiaChi', label: 'Địa Chỉ', type: 'text' },
    { name: 'SoDienThoai', label: 'Số Điện Thoại', type: 'text' },
  ],
  nongsan: [
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'TenNongSan', label: 'Tên Nông Sản', type: 'text' },
    { name: 'MaLoai', label: 'Mã Loại', type: 'text' },
    { name: 'GiaBan', label: 'Giá Bán', type: 'number' },
    { name: 'SoLuongTonKho', label: 'Số Lượng Tồn Kho', type: 'number' },
    { name: 'DonViTinh', label: 'Đơn Vị Tính', type: 'text' },
    { name: 'MaNhaCungCap', label: 'Mã Nhà Cung Cấp', type: 'text' },
    { name: 'DuongDanAnh', label: 'Đường Dẫn Ảnh', type: 'text' },
  ],
  anhnongsan: [
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'DuongDanAnh', label: 'Đường Dẫn Ảnh', type: 'text' },
  ],
  nguongoc: [
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'KhuVuc', label: 'Khu Vực', type: 'text' },
    { name: 'PhuongPhap', label: 'Phương Pháp', type: 'text' },
  ],
  khuyenmai: [
    { name: 'MaKhuyenMai', label: 'Mã Khuyến Mãi', type: 'text' },
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'MoTa', label: 'Mô Tả', type: 'text' },
    { name: 'NgayBatDau', label: 'Ngày Bắt Đầu', type: 'date' },
    { name: 'NgayKetThuc', label: 'Ngày Kết Thúc', type: 'date' },
  ],
  kho: [
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'SoLuongTonKho', label: 'Số Lượng Tồn Kho', type: 'number' },
    { name: 'NgayCapNhat', label: 'Ngày Cập Nhật', type: 'date' },
  ],
  taikhoan: [
    { name: 'MaTaiKhoan', label: 'Mã Tài Khoản', type: 'text' },
    { name: 'MatKhau', label: 'Mật Khẩu', type: 'password' },
    { name: 'LoaiTaiKhoan', label: 'Loại Tài Khoản', type: 'text' },
    { name: 'HoTen', label: 'Họ Tên', type: 'text' },
    { name: 'DiaChi', label: 'Địa Chỉ', type: 'text' },
    { name: 'SoDienThoai', label: 'Số Điện Thoại', type: 'text' },
    { name: 'Email', label: 'Email', type: 'email' },
  ],
  hoadon: [
    { name: 'MaHoaDon', label: 'Mã Hóa Đơn', type: 'text' },
    { name: 'NgayXuat', label: 'Ngày Xuất', type: 'date' },
    { name: 'TongTien', label: 'Tổng Tiền', type: 'number' },
    { name: 'MaTaiKhoan', label: 'Mã Tài Khoản', type: 'text' },
  ],
  chitiethoadon: [
    { name: 'MaHoaDon', label: 'Mã Hóa Đơn', type: 'text' },
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'SoLuong', label: 'Số Lượng', type: 'number' },
    { name: 'DonGia', label: 'Đơn Giá', type: 'number' },
    { name: 'GiamGia', label: 'Giảm Giá (%)', type: 'number' },
  ],
  cart: [
    { name: 'MaTaiKhoan', label: 'Mã Tài Khoản', type: 'text' },
    { name: 'MaNongSan', label: 'Mã Nông Sản', type: 'text' },
    { name: 'SoLuong', label: 'Số Lượng', type: 'number' },
    { name: 'GiamGia', label: 'Giảm Giá (%)', type: 'number' },
    { name: 'PhiShip', label: 'Phí Ship', type: 'number' },
  ],
};
const readOnlySections = ['hoadon', 'chitiethoadon']; // Các phần không được phép chỉnh sửa
const readOnlyFields = ['MaLoai', 'MaNongSan', 'MaHoaDon', 'MaTaiKhoan', 'MaKhuyenMai','MaNhaCungCap'];

export default function EditProductForm() {
  const { section, id } = useParams();
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!sectionsData[section]) {
      alert('Section không hợp lệ!');
      navigate('/admin');
      return;
    }

    if (readOnlySections.includes(section)) {
      alert(`Bạn không có quyền chỉnh sửa ${section}.`);
      navigate('/admin');
      return;
    }

    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/${section}/${id}`);
        if (!response.ok) {
          throw new Error('Không thể tải dữ liệu.');
        }
        const data = await response.json();
        setFormData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
        alert('Có lỗi xảy ra khi tải dữ liệu!');
        navigate('/admin');
      } finally {
        setFetching(false);
      }
    };

    fetchData();
  }, [section, id, navigate]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage('');

    try {
      const response = await fetch(`http://localhost:5000/api/${section}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const result = await response.json();
        throw new Error(result.error || 'Có lỗi xảy ra khi cập nhật dữ liệu!');
      }

      alert('Cập nhật thành công!');
      navigate('/admin');
    } catch (error) {
      console.error('Error submitting form:', error);
      setErrorMessage(error.message || 'Có lỗi xảy ra!');
    } finally {
      setLoading(false);
    }
  };

  const renderFormFields = () => {
    if (!sectionsData[section]) {
      return <div>Không có form cho loại dữ liệu này.</div>;
    }

    return sectionsData[section].map((field) => (
      <div key={field.name} className="mb-4">
        <label className="block mb-1 font-medium text-gray-700">{field.label}</label>
        <Input
          name={field.name}
          type={field.type}
          value={formData[field.name] || ''}
          onChange={handleChange}
          placeholder={`Nhập ${field.label}`}
          readOnly={readOnlyFields.includes(field.name)}
          className={`w-full p-2 border ${
            readOnlyFields.includes(field.name) ? 'bg-gray-200' : 'border-gray-300'
          } rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400`}
        />
      </div>
    ));
  };

  if (fetching) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-50">
        <div className="text-lg font-semibold text-gray-600">Đang tải dữ liệu...</div>
      </div>
    );
  }

  return (
    <div className="flex justify-center items-start p-8 min-h-screen bg-gray-50">
      <div className="w-full max-w-xl bg-white shadow-md rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-6 text-center uppercase">
          Chỉnh Sửa {section}
        </h2>

        {readOnlySections.includes(section) ? (
          <p className="text-red-600 font-semibold text-center">
            Bạn <strong>không có quyền chỉnh sửa</strong> {section}.
          </p>
        ) : (
          <form onSubmit={handleSubmit}>
            {renderFormFields()}
            {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
            <div className="text-center mt-4">
              <Button type="submit" disabled={loading}>
                {loading ? 'Đang xử lý...' : 'Cập nhật'}
              </Button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}