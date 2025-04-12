from flask import Blueprint, request, jsonify
from app import db
from app.models import NguonGoc

bp = Blueprint("nguon_goc", __name__)

# Lấy tất cả nguồn gốc
@bp.route("/", methods=["GET"])
def get_all():
    data = NguonGoc.query.all()
    result = [{
        "MaNongSan": item.MaNongSan,
        "KhuVuc": item.KhuVuc,
        "PhuongPhap": item.PhuongPhap
    } for item in data]
    return jsonify(result)

# Lấy nguồn gốc theo mã nông sản
@bp.route("/<ma>", methods=["GET"])
def get_by_id(ma):
    item = NguonGoc.query.get(ma)
    if item:
        return jsonify({
            "MaNongSan": item.MaNongSan,
            "KhuVuc": item.KhuVuc,
            "PhuongPhap": item.PhuongPhap
        })
    return jsonify({"error": "Không tìm thấy"}), 404

# Tạo mới
@bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    item = NguonGoc(
        MaNongSan=data.get("MaNongSan"),
        KhuVuc=data.get("KhuVuc"),
        PhuongPhap=data.get("PhuongPhap")
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Tạo nguồn gốc thành công"}), 201

# Cập nhật
@bp.route("/<ma>", methods=["PUT"])
def update(ma):
    item = NguonGoc.query.get(ma)
    if not item:
        return jsonify({"error": "Không tìm thấy"}), 404
    data = request.get_json()
    item.KhuVuc = data.get("KhuVuc", item.KhuVuc)
    item.PhuongPhap = data.get("PhuongPhap", item.PhuongPhap)
    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})

# Xóa
@bp.route("/<ma>", methods=["DELETE"])
def delete(ma):
    item = NguonGoc.query.get(ma)
    if not item:
        return jsonify({"error": "Không tìm thấy"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Xóa thành công"})
