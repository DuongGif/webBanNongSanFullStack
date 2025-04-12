from app import db

class NongSan(db.Model):
    __tablename__ = 'NongSan'
    MaNongSan = db.Column(db.String(10), primary_key=True)
    TenNongSan = db.Column(db.String(255), nullable=False)
    MaLoai = db.Column(db.String(10), db.ForeignKey('LoaiNongSan.MaLoai'))
    GiaBan = db.Column(db.Numeric(18, 2))
    SoLuongTonKho = db.Column(db.Integer)
    DonViTinh = db.Column(db.String(50))
    MaNhaCungCap = db.Column(db.String(10), db.ForeignKey('NhaCungCap.MaNhaCungCap'))
    DuongDanAnh = db.Column(db.String(255))
