from app import db
from app.models.tai_khoan import TaiKhoan
from app.models.nong_san import NongSan

class Cart(db.Model):
    __tablename__ = "Cart"

    MaTaiKhoan = db.Column(db.String(10), db.ForeignKey("TaiKhoan.MaTaiKhoan"), primary_key=True, nullable=False)
    MaNongSan = db.Column(db.String(10), db.ForeignKey("NongSan.MaNongSan"), primary_key=True, nullable=False)
    SoLuong = db.Column(db.Integer, nullable=False)
    GiamGia = db.Column(db.Integer)
    PhiShip = db.Column(db.Float)

    # Relationships
    taikhoan = db.relationship("TaiKhoan", backref="giohang", lazy=True)
    nongsan = db.relationship("NongSan", backref="giohang", lazy=True)
