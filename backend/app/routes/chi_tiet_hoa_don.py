from flask import Blueprint, request, jsonify
from app.models import ChiTietHoaDon
from app import db

bp = Blueprint("chi_tiet_hoa_don", __name__, url_prefix="/chi_tiet_hoa_don")

# Lấy tất cả chi tiết hóa đơn
@bp.route("/", methods=["GET"])
def get_all_chi_tiet_hoa_don():
    ds_cthd = ChiTietHoaDon.query.all()
    result = []
    for cthd in ds_cthd:
        result.append({
            "MaHoaDon": cthd.MaHoaDon,
            "MaNongSan": cthd.MaNongSan,
            "SoLuong": cthd.SoLuong,
            "DonGia": float(cthd.DonGia) if cthd.DonGia else None,
            "GiamGia": float(cthd.GiamGia) if cthd.GiamGia else None
        })
    return jsonify(result)

# Lấy chi tiết theo mã hóa đơn và mã nông sản (2 khóa chính)
@bp.route("/<ma_hoa_don>/<ma_nong_san>", methods=["GET"])
def get_chi_tiet_by_id(ma_hoa_don, ma_nong_san):
    cthd = ChiTietHoaDon.query.get((ma_hoa_don, ma_nong_san))
    if cthd:
        return jsonify({
            "MaHoaDon": cthd.MaHoaDon,
            "MaNongSan": cthd.MaNongSan,
            "SoLuong": cthd.SoLuong,
            "DonGia": float(cthd.DonGia) if cthd.DonGia else None,
            "GiamGia": float(cthd.GiamGia) if cthd.GiamGia else None
        })
    return jsonify({"error": "Không tìm thấy chi tiết hóa đơn"}), 404

# Thêm chi tiết hóa đơn
@bp.route("/", methods=["POST"])
def create_chi_tiet_hoa_don():
    data = request.get_json()
    cthd = ChiTietHoaDon(
        MaHoaDon = data.get("MaHoaDon"),
        MaNongSan = data.get("MaNongSan"),
        SoLuong = data.get("SoLuong"),
        DonGia = data.get("DonGia"),
        GiamGia = data.get("GiamGia")
    )
    db.session.add(cthd)
    db.session.commit()
    return jsonify({"message": "Tạo chi tiết hóa đơn thành công"}), 201

# Cập nhật chi tiết hóa đơn
@bp.route("/<ma_hoa_don>/<ma_nong_san>", methods=["PUT"])
def update_chi_tiet_hoa_don(ma_hoa_don, ma_nong_san):
    cthd = ChiTietHoaDon.query.get((ma_hoa_don, ma_nong_san))
    if not cthd:
        return jsonify({"error": "Không tìm thấy chi tiết hóa đơn"}), 404

    data = request.get_json()
    cthd.SoLuong = data.get("SoLuong")
    cthd.DonGia = data.get("DonGia")
    cthd.GiamGia = data.get("GiamGia")
    db.session.commit()
    return jsonify({"message": "Cập nhật chi tiết hóa đơn thành công"})

# Xóa chi tiết hóa đơn
@bp.route("/<ma_hoa_don>/<ma_nong_san>", methods=["DELETE"])
def delete_chi_tiet_hoa_don(ma_hoa_don, ma_nong_san):
    cthd = ChiTietHoaDon.query.get((ma_hoa_don, ma_nong_san))
    if not cthd:
        return jsonify({"error": "Không tìm thấy chi tiết hóa đơn"}), 404

    db.session.delete(cthd)
    db.session.commit()
    return jsonify({"message": "Xóa chi tiết hóa đơn thành công"})
