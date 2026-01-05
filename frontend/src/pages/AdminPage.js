import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DataTable from 'react-data-table-component';
import {
  FaTags, FaTruck, FaSeedling, FaImage, FaMapMarkerAlt, FaWarehouse,
  FaUserCog, FaReceipt, FaListAlt, FaShoppingCart, FaEdit, FaTrash, FaSignOutAlt
} from 'react-icons/fa';
import { Button } from '../components/ui/button';

const SECTIONS = [
  { id: 'loainongsan', icon: <FaTags />, label: 'Loại Nông Sản', endpoint: '/api/loainongsan', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaLoai'] },
  { id: 'nhacungcap', icon: <FaTruck />, label: 'Nhà Cung Cấp', endpoint: '/api/nhacungcap', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaNhaCungCap'] },
  { id: 'nongsan', icon: <FaSeedling />, label: 'Nông Sản', endpoint: '/api/nongsan', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaNongSan', 'MaLoai', 'MaNhaCungCap'] },
  { id: 'anhnongsan', icon: <FaImage />, label: 'Ảnh Nông Sản', endpoint: '/api/anhnongsan', actions: ['GET', 'POST', 'DELETE'], keys: ['MaNongSan', 'DuongDanAnh'] },
  { id: 'nguongoc', icon: <FaMapMarkerAlt />, label: 'Nguồn Gốc', endpoint: '/api/nguongoc', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaNongSan'] },
  { id: 'khuyenmai', icon: <FaTags />, label: 'Khuyến Mãi', endpoint: '/api/khuyenmai', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaKhuyenMai', 'MaNongSan'] },
  { id: 'kho', icon: <FaWarehouse />, label: 'Kho', endpoint: '/api/kho', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaNongSan'] },
  { id: 'taikhoan', icon: <FaUserCog />, label: 'Tài Khoản', endpoint: '/api/taikhoan', actions: ['GET', 'POST', 'PUT', 'DELETE'], keys: ['MaTaiKhoan'] },
  { id: 'hoadon', icon: <FaReceipt />, label: 'Hóa Đơn', endpoint: '/api/hoadon', actions: ['GET'], keys: ['MaHoaDon', 'MaTaiKhoan'] },
  { id: 'chitiethoadon', icon: <FaListAlt />, label: 'Chi Tiết HĐ', endpoint: '/api/chitiethoadon', actions: ['GET'], keys: ['MaHoaDon', 'MaNongSan'] },
  { id: 'cart', icon: <FaShoppingCart />, label: 'Giỏ Hàng', endpoint: '/api/cart', actions: ['GET', 'POST', 'DELETE'], keys: ['MaTaiKhoan', 'MaNongSan'] },
  { id: 'contact', icon: <FaListAlt />, label: 'Liên Hệ Người Dùng', endpoint: '/api/contact', actions: ['GET'], keys: ['MaContact'] }
];

export default function AdminPage() {
  const navigate = useNavigate();
  const [currentSection, setCurrentSection] = useState(SECTIONS[0].id);
  const [data, setData] = useState([]);
  const [pagination, setPagination] = useState(null);
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    fetchData();
  }, [currentSection]);

  async function fetchData(page = 1) {
    try {
      const response = await fetch(`http://localhost:5000/api/${currentSection}?page=${page}`);
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const result = await response.json();
      const dataItems = result.items || result;

      setData(dataItems);
      setPagination(result.pagination || null);

      if (dataItems.length > 0) {
        const dynamicColumns = Object.keys(dataItems[0]).map(key => ({
          name: key,
          selector: row => row[key],
          sortable: true,
        }));

        setColumns([
          ...dynamicColumns,
          {
            name: 'Hành động',
            cell: (row) => {
              const section = SECTIONS.find(s => s.id === currentSection);
              const primaryKey = getPrimaryKeyForSection(row);

              if (['hoadon', 'chitiethoadon', 'taikhoan'].includes(section.id)) {
                return <span className="text-gray-500">Không khả dụng</span>;
              }

              return (
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    onClick={() => navigate(`/admin/${currentSection}/edit/${encodeURIComponent(primaryKey)}`)}
                  >
                    <FaEdit />
                  </Button>
                  <Button
                    size="sm"
                    variant="destructive"
                    onClick={() => handleDelete(primaryKey)}
                  >
                    <FaTrash />
                  </Button>
                </div>
              );
            },
          },
        ]);
      } else {
        setColumns([]);
      }
    } catch (error) {
      console.error('Error fetching data:', error.message || error);
      setData([]);
      setColumns([]);
    }
  }

  const getPrimaryKeyForSection = (row) => {
    const section = SECTIONS.find(s => s.id === currentSection);
    if (!section || !section.keys || section.keys.length === 0) return null;
    return row[section.keys[0]];
  };

  const handleDelete = async (primaryKey) => {
    const section = SECTIONS.find(s => s.id === currentSection);
    if (['hoadon', 'chitiethoadon'].includes(section.id)) return;

    try {
      const response = await fetch(`http://localhost:5000/api/${currentSection}/${encodeURIComponent(primaryKey)}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      setData(prev => prev.filter(row => row[section.keys[0]] !== primaryKey));
    } catch (error) {
      console.error('Error deleting record:', error.message || error);
    }
  };

  const changePage = (newPage) => {
    fetchData(newPage);
  };

  const handleAddNew = () => {
    const section = SECTIONS.find(s => s.id === currentSection);
    if (['hoadon', 'chitiethoadon', 'contact'].includes(section.id)) return;
    navigate(`/admin/${currentSection}/add`);
  };

  const handleLogout = () => {
    localStorage.clear();
    sessionStorage.clear();
    navigate('/');
    window.location.reload();
  };

  return (
    <div className="admin-page-container min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100 p-4">
      <header className="bg-green-600 text-white p-6 rounded-xl mb-6 shadow-lg flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-wide">🌿 Trang Quản Trị Hệ Thống</h1>
        <Button variant="destructive" onClick={handleLogout}>
          <FaSignOutAlt className="mr-2" /> Đăng Xuất
        </Button>
      </header>

      <div className="flex gap-4">
        <aside className="w-64 bg-white rounded-xl shadow-md p-4 space-y-2 sticky top-4">
          <h2 className="text-lg font-semibold text-gray-600 mb-3">📁 Danh Mục</h2>
          {SECTIONS.map(s => (
            <Button
              key={s.id}
              variant={s.id === currentSection ? 'default' : 'outline'}
              disabled={s.id === currentSection}
              className={`w-full justify-start font-medium text-left transition-all ${
                s.id === currentSection
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'text-gray-700 hover:bg-green-100'
              }`}
              onClick={() => setCurrentSection(s.id)}
            >
              <span className="mr-2 text-lg">{s.icon}</span>
              {s.label}
            </Button>
          ))}
        </aside>

        <main className="flex-1 bg-white rounded-xl shadow-md p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-green-700">{SECTIONS.find(s => s.id === currentSection)?.label}</h2>
            <Button onClick={handleAddNew} className="bg-green-500 hover:bg-green-600 text-white">
              ➕ Thêm mới
            </Button>
          </div>

          {data.length > 0 ? (
            <>
              <div className="rounded overflow-hidden border border-gray-200 shadow-sm">
                <DataTable
                  columns={columns}
                  data={data}
                  pagination
                  highlightOnHover
                  responsive
                  customStyles={{
                    rows: { style: { minHeight: '60px' } },
                    headCells: {
                      style: {
                        backgroundColor: '#f0fdf4',
                        color: '#166534',
                        fontWeight: 'bold',
                      },
                    },
                  }}
                />
              </div>
              {pagination && (
                <div className="flex justify-between items-center mt-6 text-sm text-gray-700">
                  <Button
                    disabled={!pagination.has_prev}
                    onClick={() => changePage(pagination.page - 1)}
                    className="bg-gray-200 hover:bg-gray-300"
                  >
                    ◀ Trang trước
                  </Button>
                  <span>Trang {pagination.page} / {pagination.pages}</span>
                  <Button
                    disabled={!pagination.has_next}
                    onClick={() => changePage(pagination.page + 1)}
                    className="bg-gray-200 hover:bg-gray-300"
                  >
                    Trang sau ▶
                  </Button>
                </div>
              )}
            </>
          ) : (
            <div className="text-center text-gray-500 text-lg">📭 Không có dữ liệu để hiển thị.</div>
          )}
        </main>
      </div>
    </div>
  );
}
