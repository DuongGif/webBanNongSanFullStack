from app import db

class ChiTietHoaDon(db.Model):
    __tablename__ = "ChiTietHoaDon"
    MaHoaDon = db.Column(db.String(10), db.ForeignKey("HoaDon.MaHoaDon"), primary_key=True)
    MaNongSan = db.Column(db.String(10), db.ForeignKey("NongSan.MaNongSan"), primary_key=True)
    SoLuong = db.Column(db.Integer)
    DonGia = db.Column(db.Float)
    GiamGia = db.Column(db.Float)