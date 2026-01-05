from flask_sqlalchemy import SQLAlchemy

from app import db  # Import db từ app/__init__.py

# Import tất cả các model
from .loai_nong_san import LoaiNongSan
from .nha_cung_cap import NhaCungCap
from .nong_san import NongSan
from .hoa_don import HoaDon
from .chi_tiet_hoa_don import ChiTietHoaDon
from .kho import Kho
from .tai_khoan import TaiKhoan
from .khuyen_mai import KhuyenMai
from .nguon_goc import NguonGoc
from .anh_nong_san import AnhNongSan
from .cart import Cart
from .review import review
from .contact import Contact
