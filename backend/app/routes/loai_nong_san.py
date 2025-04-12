from flask import Blueprint, jsonify, request
from app.models import LoaiNongSan
from app import db

bp = Blueprint('loai_nong_san', __name__, url_prefix="/loai_nong_san")

# Lấy tất cả loại nông sản
@bp.route("/", methods=["GET"])
def get_loai_nongsan():
    loai_list = LoaiNongSan.query.all()
    result = []
    for loai in loai_list:
        result.append({
            "MaLoai": loai.MaLoai,
            "TenLoai": loai.TenLoai
        })
    return jsonify(result)

# Lấy 1 loại theo mã
@bp.route("/<ma_loai>", methods=["GET"])
def get_loai_by_id(ma_loai):
    loai = LoaiNongSan.query.get(ma_loai)
    if loai:
        return jsonify({
            "MaLoai": loai.MaLoai,
            "TenLoai": loai.TenLoai
        })
    return jsonify({"error": "Không tìm thấy loại nông sản"}), 404

# Thêm loại nông sản
@bp.route("/", methods=["POST"])
def create_loai_nongsan():
    data = request.get_json()
    loai = LoaiNongSan(
        MaLoai = data.get("MaLoai"),
        TenLoai = data.get("TenLoai")
    )
    db.session.add(loai)
    db.session.commit()
    return jsonify({"message": "Tạo loại nông sản thành công"}), 201

# Cập nhật loại nông sản
@bp.route("/<ma_loai>", methods=["PUT"])
def update_loai_nongsan(ma_loai):
    loai = LoaiNongSan.query.get(ma_loai)
    if not loai:
        return jsonify({"error": "Không tìm thấy loại nông sản"}), 404

    data = request.get_json()
    loai.TenLoai = data.get("TenLoai", loai.TenLoai)
    db.session.commit()
    return jsonify({"message": "Cập nhật loại nông sản thành công"})

# Xóa loại nông sản
@bp.route("/<ma_loai>", methods=["DELETE"])
def delete_loai_nongsan(ma_loai):
    loai = LoaiNongSan.query.get(ma_loai)
    if not loai:
        return jsonify({"error": "Không tìm thấy loại nông sản"}), 404

    db.session.delete(loai)
    db.session.commit()
    return jsonify({"message": "Xóa loại nông sản thành công"})
