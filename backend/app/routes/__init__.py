from .nong_san import bp as nong_san_bp
from .loai_nong_san import bp as loai_nong_san_bp
from .nha_cung_cap import bp as nha_cung_cap_bp
from .hoa_don import bp as hoa_don_bp
from .chi_tiet_hoa_don import bp as chi_tiet_hoa_don_bp
from .tai_khoan import bp as tai_khoan_bp
from .kho import bp as kho_bp
from .khuyen_mai import bp as khuyen_mai_bp
from .nguon_goc import bp as nguon_goc_bp
from .anh_nong_san import bp as anh_nong_san_bp
from .cart import cart_bp  # Thêm import cho cart_bp
from .review import bp as review_bp
from .contact import contact_bp

def register_routes(app):
    app.register_blueprint(contact_bp)
    app.register_blueprint(nong_san_bp)
    app.register_blueprint(loai_nong_san_bp)
    app.register_blueprint(nha_cung_cap_bp)
    app.register_blueprint(hoa_don_bp)
    app.register_blueprint(chi_tiet_hoa_don_bp)
    app.register_blueprint(tai_khoan_bp)
    app.register_blueprint(kho_bp)
    app.register_blueprint(khuyen_mai_bp)
    app.register_blueprint(nguon_goc_bp)
    app.register_blueprint(anh_nong_san_bp)
    app.register_blueprint(cart_bp)  # Đăng ký cart blueprint
    app.register_blueprint(review_bp)
