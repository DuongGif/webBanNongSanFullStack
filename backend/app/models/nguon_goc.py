from app import db

class NguonGoc(db.Model):
    __tablename__ = 'NguonGoc'
    MaNongSan = db.Column(db.String(10), db.ForeignKey('NongSan.MaNongSan'), primary_key=True)
    KhuVuc = db.Column(db.String(100))
    PhuongPhap = db.Column(db.String(100))
