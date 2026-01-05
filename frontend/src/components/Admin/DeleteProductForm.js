import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/button';
import { Input } from '../ui/input';

const primaryKeyFields = {
  loainongsan: 'MaLoai',
  nhacungcap: 'MaNhaCungCap',
  nongsan: 'MaNongSan',
  anhnongsan: 'MaNongSan',
  nguongoc: 'MaNongSan',
  khuyenmai: 'MaKhuyenMai',
  kho: 'MaNongSan',
  taikhoan: 'MaTaiKhoan',
  hoadon: 'MaHoaDon',
  chitiethoadon: ['MaHoaDon', 'MaNongSan'], // Composite key
  cart: ['MaTaiKhoan', 'MaNongSan'], // Composite key
};

const restrictedSections = ['chitiethoadon','hoadon']; // Các phần không được phép xóa

export default function DeleteProductForm() {
  const { section } = useParams();
  const [idToDelete, setIdToDelete] = useState({});
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!primaryKeyFields[section]) {
      alert('Section không hợp lệ!');
      navigate('/admin');
      return;
    }

    if (restrictedSections.includes(section)) {
      alert(`Bạn không được phép xóa dữ liệu trong phần ${section}.`);
      navigate('/admin');
    }
  }, [section, navigate]);

  const handleInputChange = (key, value) => {
    setIdToDelete((prev) => ({ ...prev, [key]: value }));
  };

  const handleDelete = async () => {
    setMessage('');
    try {
      const queryParams = new URLSearchParams(idToDelete).toString();
      const response = await fetch(`http://localhost:5000/api/${section}?${queryParams}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const result = await response.json();
        throw new Error(result.error || 'Xóa thất bại!');
      }

      alert('Xóa thành công!');
      navigate('/admin');
    } catch (error) {
      console.error('Lỗi khi xóa:', error);
      setMessage(error.message || 'Có lỗi xảy ra khi gửi yêu cầu xóa.');
    }
  };

  const renderInputFields = () => {
    const keys = Array.isArray(primaryKeyFields[section])
      ? primaryKeyFields[section]
      : [primaryKeyFields[section]];

    return keys.map((key) => (
      <div key={key} className="mb-4">
        <label className="block mb-1 font-medium text-gray-700">{key}</label>
        <Input
          type="text"
          value={idToDelete[key] || ''}
          onChange={(e) => handleInputChange(key, e.target.value)}
          placeholder={`Nhập ${key}`}
          className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400"
        />
      </div>
    ));
  };

  return (
    <div className="flex justify-center items-start p-8 min-h-screen bg-gray-50">
      <div className="w-full max-w-xl bg-white shadow-md rounded-lg p-8">
        <h2 className="text-2xl font-bold mb-6 text-center uppercase">
          Xóa {section}
        </h2>

        {message && <p className="text-red-500 mb-4">{message}</p>}

        {restrictedSections.includes(section) ? (
          <p className="text-red-600 text-center">
            Bạn <strong>không được phép xóa</strong> dữ liệu trong phần {section}.
          </p>
        ) : (
          <>
            {renderInputFields()}
            <div className="text-center">
              <Button
                variant="destructive"
                onClick={handleDelete}
                disabled={Object.values(idToDelete).some((value) => !value.trim())}
              >
                Xác nhận xóa
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
