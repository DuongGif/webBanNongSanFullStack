from app import db

class TaiKhoan(db.Model):
    __tablename__ = "TaiKhoan"
    MaTaiKhoan = db.Column(db.String(10), primary_key=True)
    MatKhau = db.Column(db.String(50), nullable=False)
    LoaiTaiKhoan = db.Column(db.String(10), nullable=False)
    HoTen = db.Column(db.String(100), nullable=False)
    DiaChi = db.Column(db.String(200))
    SoDienThoai = db.Column(db.String(20))
    Email = db.Column(db.String(100))

    hoa_don = db.relationship("HoaDon", backref="taikhoan", lazy=True)
