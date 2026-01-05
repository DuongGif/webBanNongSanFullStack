from flask import Blueprint, jsonify, request
from app.models import NhaCungCap
from app import db
from flask_cors import cross_origin
from app.models import db, NhaCungCap  

bp = Blueprint('nha_cung_cap', __name__)

# Lấy tất cả nhà cung cấp (không phân trang)
@bp.route("/", methods=["GET"])
def get_nha_cung_cap():
    ncc_list = NhaCungCap.query.all()  # Lấy tất cả nhà cung cấp mà không phân trang
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
    if not ncc:
        return jsonify({"status": "error", "message": "Không tìm thấy nhà cung cấp"}), 404
    return jsonify({

            "MaNhaCungCap": ncc.MaNhaCungCap,
            "TenNhaCungCap": ncc.TenNhaCungCap,
            "DiaChi": ncc.DiaChi,
            "SoDienThoai": ncc.SoDienThoai
        
    })


@bp.route("", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create_nha_cung_cap():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()

    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    ncc = NhaCungCap(
        MaNhaCungCap=data.get("MaNhaCungCap"),
        TenNhaCungCap=data.get("TenNhaCungCap"),
        DiaChi=data.get("DiaChi"),
        SoDienThoai=data.get("SoDienThoai")
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
