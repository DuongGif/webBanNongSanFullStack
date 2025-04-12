from .. import db

class AnhNongSan(db.Model):
    __tablename__ = 'AnhNongSan'
    MaNongSan = db.Column(db.String(10), db.ForeignKey('NongSan.MaNongSan', ondelete='CASCADE'), primary_key=True)
    DuongDanAnh = db.Column(db.String(255), primary_key=True)
