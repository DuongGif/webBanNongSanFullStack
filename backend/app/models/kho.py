from app import db

class Kho(db.Model):
    __tablename__ = "Kho"
    MaNongSan = db.Column(db.String(10), db.ForeignKey("NongSan.MaNongSan"), primary_key=True)
    SoLuongTonKho = db.Column(db.Integer)
    NgayCapNhat = db.Column(db.Date)
    nongsan = db.relationship("NongSan", backref=db.backref("kho", uselist=False))
