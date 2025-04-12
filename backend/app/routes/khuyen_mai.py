from flask import Blueprint, request, jsonify
from app import db
from app.models import KhuyenMai

bp = Blueprint("khuyen_mai", __name__)

# Lấy tất cả khuyến mãi
@bp.route("/", methods=["GET"])
def get_all():
    kms = KhuyenMai.query.all()
    result = [{
        "MaKhuyenMai": km.MaKhuyenMai,
        "MaNongSan": km.MaNongSan,
        "MoTa": km.MoTa,
        "NgayBatDau": km.NgayBatDau.strftime("%Y-%m-%d") if km.NgayBatDau else None,
        "NgayKetThuc": km.NgayKetThuc.strftime("%Y-%m-%d") if km.NgayKetThuc else None
    } for km in kms]
    return jsonify(result)

# Lấy khuyến mãi theo mã
@bp.route("/<ma>", methods=["GET"])
def get_by_id(ma):
    km = KhuyenMai.query.get(ma)
    if km:
        return jsonify({
            "MaKhuyenMai": km.MaKhuyenMai,
            "MaNongSan": km.MaNongSan,
            "MoTa": km.MoTa,
            "NgayBatDau": km.NgayBatDau.strftime("%Y-%m-%d") if km.NgayBatDau else None,
            "NgayKetThuc": km.NgayKetThuc.strftime("%Y-%m-%d") if km.NgayKetThuc else None
        })
    return jsonify({"error": "Không tìm thấy"}), 404

# Tạo mới khuyến mãi
@bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    km = KhuyenMai(
        MaKhuyenMai=data.get("MaKhuyenMai"),
        MaNongSan=data.get("MaNongSan"),
        MoTa=data.get("MoTa"),
        NgayBatDau=data.get("NgayBatDau"),
        NgayKetThuc=data.get("NgayKetThuc")
    )
    db.session.add(km)
    db.session.commit()
    return jsonify({"message": "Tạo khuyến mãi thành công"}), 201

# Cập nhật khuyến mãi
@bp.route("/<ma>", methods=["PUT"])
def update(ma):
    km = KhuyenMai.query.get(ma)
    if not km:
        return jsonify({"error": "Không tìm thấy"}), 404
    data = request.get_json()
    km.MaNongSan = data.get("MaNongSan", km.MaNongSan)
    km.MoTa = data.get("MoTa", km.MoTa)
    km.NgayBatDau = data.get("NgayBatDau", km.NgayBatDau)
    km.NgayKetThuc = data.get("NgayKetThuc", km.NgayKetThuc)
    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})

# Xóa khuyến mãi
@bp.route("/<ma>", methods=["DELETE"])
def delete(ma):
    km = KhuyenMai.query.get(ma)
    if not km:
        return jsonify({"error": "Không tìm thấy"}), 404
    db.session.delete(km)
    db.session.commit()
    return jsonify({"message": "Xóa thành công"})
