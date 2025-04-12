from flask import Blueprint, request, jsonify
from app import db
from app.models import AnhNongSan

bp = Blueprint("anh_nong_san", __name__)

# Lấy tất cả ảnh
@bp.route("/", methods=["GET"])
def get_all():
    data = AnhNongSan.query.all()
    result = [{
        "MaNongSan": item.MaNongSan,
        "DuongDanAnh": item.DuongDanAnh
    } for item in data]
    return jsonify(result)

# Lấy ảnh theo mã nông sản
@bp.route("/<ma>", methods=["GET"])
def get_by_ma(ma):
    data = AnhNongSan.query.filter_by(MaNongSan=ma).all()
    result = [{
        "MaNongSan": item.MaNongSan,
        "DuongDanAnh": item.DuongDanAnh
    } for item in data]
    return jsonify(result)

# Thêm ảnh
@bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    item = AnhNongSan(
        MaNongSan=data.get("MaNongSan"),
        DuongDanAnh=data.get("DuongDanAnh")
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Thêm ảnh thành công"}), 201

# Xóa ảnh
@bp.route("/", methods=["DELETE"])
def delete():
    data = request.get_json()
    ma = data.get("MaNongSan")
    duong_dan = data.get("DuongDanAnh")
    item = AnhNongSan.query.get((ma, duong_dan))
    if not item:
        return jsonify({"error": "Không tìm thấy ảnh"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Xóa ảnh thành công"})
