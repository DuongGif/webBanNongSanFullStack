from app import db

class NhaCungCap(db.Model):
    __tablename__ = 'NhaCungCap'
    MaNhaCungCap = db.Column(db.String(10), primary_key=True)
    TenNhaCungCap = db.Column(db.String(100), nullable=False)
    DiaChi = db.Column(db.String(255))
    SoDienThoai = db.Column(db.String(15))

    nong_san = db.relationship('NongSan', backref='nhacungcap', lazy=True)
