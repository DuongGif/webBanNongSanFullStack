import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ Cấu hình CORS cho cả localhost và 127.0.0.1
    CORS(app, resources={r"/*": {"origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]}}, supports_credentials=True)

    # Load cấu hình từ file config.py
    app.config.from_object('app.config.Config')

    # Khởi tạo database
    db.init_app(app)

    # Import và đăng ký các Blueprint
    from app.routes.nong_san import bp as nong_san_bp
    from app.routes.loai_nong_san import bp as loai_nong_san_bp
    from app.routes.nha_cung_cap import bp as nha_cung_cap_bp
    from app.routes.hoa_don import bp as hoa_don_bp
    from app.routes.chi_tiet_hoa_don import bp as chi_tiet_hoa_don_bp
    from app.routes.kho import bp as kho_bp
    from app.routes.tai_khoan import bp as tai_khoan_bp
    from app.routes.khuyen_mai import bp as khuyen_mai_bp
    from app.routes.nguon_goc import bp as nguon_goc_bp
    from app.routes.anh_nong_san import bp as anh_nong_san_bp

    # Đăng ký route API
    app.register_blueprint(nong_san_bp, url_prefix="/api/nongsan")
    app.register_blueprint(loai_nong_san_bp, url_prefix="/api/loainongsan")
    app.register_blueprint(nha_cung_cap_bp, url_prefix="/api/nhacungcap")
    app.register_blueprint(hoa_don_bp, url_prefix="/api/hoadon")
    app.register_blueprint(chi_tiet_hoa_don_bp, url_prefix="/api/chitiethoadon")
    app.register_blueprint(kho_bp, url_prefix="/api/kho")
    app.register_blueprint(tai_khoan_bp, url_prefix="/api/taikhoan")
    app.register_blueprint(khuyen_mai_bp, url_prefix="/api/khuyenmai")
    app.register_blueprint(nguon_goc_bp, url_prefix="/api/nguongoc")
    app.register_blueprint(anh_nong_san_bp, url_prefix="/api/anhnongsan")

    # Trang chủ test
    @app.route("/")
    def home():
        return "Trang chủ API QLNongSan"

    return app
