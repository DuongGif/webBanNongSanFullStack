from app import db

class review(db.Model):
    __tablename__ = 'Review'
    
    MaReview = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaTaiKhoan = db.Column(db.String(10), db.ForeignKey('TaiKhoan.MaTaiKhoan', ondelete='CASCADE'), nullable=True)
    Email = db.Column(db.String(100), nullable=True)
    MaNongSan = db.Column(db.String(10), db.ForeignKey('NongSan.MaNongSan', ondelete='CASCADE'), nullable=True)
    NoiDung = db.Column(db.Text, nullable=False)
