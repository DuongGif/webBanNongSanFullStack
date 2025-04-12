from app import db

class KhuyenMai(db.Model):
    __tablename__ = 'KhuyenMai'
    MaKhuyenMai = db.Column(db.String(10), primary_key=True)
    MaNongSan = db.Column(db.String(10), db.ForeignKey('NongSan.MaNongSan'))
    MoTa = db.Column(db.String(255))
    NgayBatDau = db.Column(db.Date)
    NgayKetThuc = db.Column(db.Date)
