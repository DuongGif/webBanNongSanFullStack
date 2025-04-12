from app import db

class HoaDon(db.Model):
    __tablename__ = "HoaDon"
    MaHoaDon = db.Column(db.String(10), primary_key=True)
    MaTaiKhoan = db.Column(db.String(10), db.ForeignKey("TaiKhoan.MaTaiKhoan"))
    NgayXuat = db.Column(db.Date)
    TongTien = db.Column(db.Float)
