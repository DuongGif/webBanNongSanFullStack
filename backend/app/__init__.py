import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail  # ✅ Thêm dòng này

db = SQLAlchemy()
mail = Mail()  # ✅ Tạo đối tượng mail

def create_app():
    app = Flask(__name__)

    # Cấu hình email (trước config object nếu muốn ghi đè)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'phamtrunghieu201004@gmail.com'
    app.config['MAIL_PASSWORD'] = 'siiu vpij jxfw laqv'
    app.config['MAIL_DEFAULT_SENDER'] = 'phamtrunghieu201004@gmail.com'  

    # ✅ Cấu hình CORS
    CORS(app, resources={r"/*": {"origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]}}, supports_credentials=True
    )
    # Load cấu hình từ class Config (nếu cần)
    app.config.from_object('app.config.Config')
    app.config['JSON_AS_ASCII'] = False

    # Khởi tạo DB và Mail
    db.init_app(app)
    mail.init_app(app)  # ✅ Khởi tạo mail

    # Import các Blueprint
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
    from app.routes.payment import payment_bp
    from app.routes.otp import bp as otp_bp
    from app.routes.cart import cart_bp
    from app.routes.review import bp as review_bp
    from app.routes.contact import contact_bp

    # Đăng ký Blueprint
    app.register_blueprint(payment_bp)
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
    app.register_blueprint(otp_bp, url_prefix="/api/otp")
    app.register_blueprint(cart_bp,url_prefix="/api/cart")
    app.register_blueprint(review_bp, url_prefix="/api/review")
    app.register_blueprint(contact_bp, url_prefix="/api/contact")

    @app.route("/")
    def home():
        return "Trang chủ API QLNongSan"

    return app
