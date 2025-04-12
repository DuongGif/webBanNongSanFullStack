from flask import Blueprint, request, jsonify
from app.models import Kho
from app import db
from datetime import datetime

bp = Blueprint("kho", __name__, url_prefix="/kho")

# Lấy danh sách toàn bộ kho
@bp.route("/", methods=["GET"])
def get_all_kho():
    ds_kho = Kho.query.all()
    result = []
    for k in ds_kho:
        result.append({
            "MaNongSan": k.MaNongSan,
            "SoLuongTonKho": k.SoLuongTonKho,
            "NgayCapNhat": k.NgayCapNhat.strftime("%Y-%m-%d") if k.NgayCapNhat else None
        })
    return jsonify(result)

# Thêm mới thông tin kho
@bp.route("/", methods=["POST"])
def create_kho():
    data = request.get_json()
    kho = Kho(
        MaNongSan = data.get("MaNongSan"),
        SoLuongTonKho = data.get("SoLuongTonKho"),
        NgayCapNhat = datetime.strptime(data.get("NgayCapNhat"), "%Y-%m-%d") if data.get("NgayCapNhat") else None
    )
    db.session.add(kho)
    db.session.commit()
    return jsonify({"message": "Thêm kho thành công"}), 201

# Cập nhật thông tin kho
@bp.route("/<ma_nongsan>", methods=["PUT"])
def update_kho(ma_nongsan):
    kho = Kho.query.get(ma_nongsan)
    if not kho:
        return jsonify({"error": "Không tìm thấy kho"}), 404

    data = request.get_json()
    kho.SoLuongTonKho = data.get("SoLuongTonKho", kho.SoLuongTonKho)
    if data.get("NgayCapNhat"):
        kho.NgayCapNhat = datetime.strptime(data.get("NgayCapNhat"), "%Y-%m-%d")
    
    db.session.commit()
    return jsonify({"message": "Cập nhật kho thành công"})

# Xóa thông tin kho
@bp.route("/<ma_nongsan>", methods=["DELETE"])
def delete_kho(ma_nongsan):
    kho = Kho.query.get(ma_nongsan)
    if not kho:
        return jsonify({"error": "Không tìm thấy kho"}), 404

    db.session.delete(kho)
    db.session.commit()
    return jsonify({"message": "Xóa kho thành công"})
# Lấy thông tin kho theo mã nông sản
@bp.route("/<ma_nongsan>", methods=["GET"])
def get_kho_by_ma_nongsan(ma_nongsan):
    kho = Kho.query.get(ma_nongsan)
    if not kho:
        return jsonify({"error": "Không tìm thấy kho với mã nông sản này"}), 404

    result = {
        "MaNongSan": kho.MaNongSan,
        "SoLuongTonKho": kho.SoLuongTonKho,
        "NgayCapNhat": kho.NgayCapNhat.strftime("%Y-%m-%d") if kho.NgayCapNhat else None
    }
    return jsonify(result)
