from app import db

class LoaiNongSan(db.Model):
    __tablename__ = 'LoaiNongSan'
    MaLoai = db.Column(db.String(10), primary_key=True)
    TenLoai = db.Column(db.String(50), nullable=False)

    nong_san = db.relationship('NongSan', backref='loai', lazy=True)
