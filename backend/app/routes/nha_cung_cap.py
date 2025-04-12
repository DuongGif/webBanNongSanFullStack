from flask import Blueprint, jsonify, request
from app.models import NhaCungCap
from app import db

bp = Blueprint('nha_cung_cap', __name__, url_prefix="/nha_cung_cap")

# Lấy tất cả nhà cung cấp
@bp.route("/", methods=["GET"])
def get_nha_cung_cap():
    ncc_list = NhaCungCap.query.all()
    result = []
    for ncc in ncc_list:
        result.append({
            "MaNhaCungCap": ncc.MaNhaCungCap,
            "TenNhaCungCap": ncc.TenNhaCungCap,
            "DiaChi": ncc.DiaChi,
            "SoDienThoai": ncc.SoDienThoai
        })
    return jsonify(result)

# Lấy nhà cung cấp theo mã
@bp.route("/<ma_ncc>", methods=["GET"])
def get_ncc_by_id(ma_ncc):
    ncc = NhaCungCap.query.get(ma_ncc)
    if ncc:
        return jsonify({
            "MaNhaCungCap": ncc.MaNhaCungCap,
            "TenNhaCungCap": ncc.TenNhaCungCap,
            "DiaChi": ncc.DiaChi,
            "SoDienThoai": ncc.SoDienThoai
        })
    return jsonify({"error": "Không tìm thấy nhà cung cấp"}), 404

# Tạo nhà cung cấp
@bp.route("/", methods=["POST"])
def create_nha_cung_cap():
    data = request.get_json()
    ncc = NhaCungCap(
        MaNhaCungCap = data.get("MaNhaCungCap"),
        TenNhaCungCap = data.get("TenNhaCungCap"),
        DiaChi = data.get("DiaChi"),
        SoDienThoai = data.get("SoDienThoai")
    )
    db.session.add(ncc)
    db.session.commit()
    return jsonify({"message": "Tạo nhà cung cấp thành công"}), 201

# Cập nhật nhà cung cấp
@bp.route("/<ma_ncc>", methods=["PUT"])
def update_nha_cung_cap(ma_ncc):
    ncc = NhaCungCap.query.get(ma_ncc)
    if not ncc:
        return jsonify({"error": "Không tìm thấy nhà cung cấp"}), 404

    data = request.get_json()
    ncc.TenNhaCungCap = data.get("TenNhaCungCap", ncc.TenNhaCungCap)
    ncc.DiaChi = data.get("DiaChi", ncc.DiaChi)
    ncc.SoDienThoai = data.get("SoDienThoai", ncc.SoDienThoai)
    db.session.commit()
    return jsonify({"message": "Cập nhật nhà cung cấp thành công"})

# Xóa nhà cung cấp
@bp.route("/<ma_ncc>", methods=["DELETE"])
def delete_nha_cung_cap(ma_ncc):
    ncc = NhaCungCap.query.get(ma_ncc)
    if not ncc:
        return jsonify({"error": "Không tìm thấy nhà cung cấp"}), 404

    db.session.delete(ncc)
    db.session.commit()
    return jsonify({"message": "Xóa nhà cung cấp thành công"})
