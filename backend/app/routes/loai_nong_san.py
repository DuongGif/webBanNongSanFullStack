from flask import Blueprint, jsonify, request
from app.models import LoaiNongSan
from flask_cors import cross_origin
from app.models import db, LoaiNongSan  ,NongSan
from app import db

bp = Blueprint('loai_nong_san', __name__)

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


@bp.route("", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create_loai_nongsan():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()

    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    loai = LoaiNongSan(
        MaLoai=data.get("MaLoai"),
        TenLoai=data.get("TenLoai")
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
    try:
        # Tìm loại nông sản theo mã loại
        loai = LoaiNongSan.query.get(ma_loai)
        if not loai:
            return jsonify({"error": "Không tìm thấy loại nông sản"}), 404

        # Tìm tất cả nông sản liên quan đến mã loại
        nongsan_list = NongSan.query.filter_by(MaLoai=ma_loai).all()

        # Xóa từng nông sản liên quan
        for nongsan in nongsan_list:
            db.session.delete(nongsan)

        # Sau khi xóa các nông sản, xóa loại nông sản
        db.session.delete(loai)
        db.session.commit()

        return jsonify({"message": "Xóa loại nông sản và tất cả nông sản liên quan thành công"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Đã xảy ra lỗi", "details": str(e)}), 500

