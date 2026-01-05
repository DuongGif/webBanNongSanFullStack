from app import db
from app.models.tai_khoan import TaiKhoan

class Contact(db.Model):
    __tablename__ = "Contact"

    MaContact = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = db.Column(db.String(10), db.ForeignKey("TaiKhoan.MaTaiKhoan"))
    Email = db.Column(db.String(100))
    TenNguoiGui = db.Column(db.String(100))
    TieuDe = db.Column(db.String(255))
    TinNhan = db.Column(db.String(255), nullable=False)

    # Relationship
    taikhoan = db.relationship("TaiKhoan", backref="lienhe", lazy=True)
