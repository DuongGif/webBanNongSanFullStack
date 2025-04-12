from flask import Blueprint, request, jsonify
from app.models import HoaDon
from app import db
from datetime import datetime

bp = Blueprint("hoa_don", __name__, url_prefix="/hoa_don")

# Lấy tất cả hóa đơn
@bp.route("/", methods=["GET"])
def get_all_hoa_don():
    ds_hoa_don = HoaDon.query.all()
    result = []
    for hd in ds_hoa_don:
        result.append({
            "MaHoaDon": hd.MaHoaDon,
            "MaTaiKhoan": hd.MaTaiKhoan,
            "NgayXuat": hd.NgayXuat.strftime("%Y-%m-%d") if hd.NgayXuat else None,
            "TongTien": float(hd.TongTien) if hd.TongTien else None
        })
    return jsonify(result)

# Lấy hóa đơn theo ID
@bp.route("/<ma>", methods=["GET"])
def get_hoa_don_by_id(ma):
    hd = HoaDon.query.get(ma)
    if hd:
        return jsonify({
            "MaHoaDon": hd.MaHoaDon,
            "MaTaiKhoan": hd.MaTaiKhoan,
            "NgayXuat": hd.NgayXuat.strftime("%Y-%m-%d") if hd.NgayXuat else None,
            "TongTien": float(hd.TongTien) if hd.TongTien else None
        })
    return jsonify({"error": "Không tìm thấy hóa đơn"}), 404

# Thêm mới hóa đơn
@bp.route("/", methods=["POST"])
def create_hoa_don():
    data = request.get_json()
    hd = HoaDon(
        MaHoaDon = data.get("MaHoaDon"),
        MaTaiKhoan = data.get("MaTaiKhoan"),
        NgayXuat = datetime.strptime(data.get("NgayXuat"), "%Y-%m-%d"),
        TongTien = data.get("TongTien")
    )
    db.session.add(hd)
    db.session.commit()
    return jsonify({"message": "Tạo hóa đơn thành công"}), 201

# Cập nhật hóa đơn
@bp.route("/<ma>", methods=["PUT"])
def update_hoa_don(ma):
    hd = HoaDon.query.get(ma)
    if not hd:
        return jsonify({"error": "Không tìm thấy hóa đơn"}), 404

    data = request.get_json()
    hd.MaTaiKhoan = data.get("MaTaiKhoan")
    hd.NgayXuat = datetime.strptime(data.get("NgayXuat"), "%Y-%m-%d")
    hd.TongTien = data.get("TongTien")
    db.session.commit()
    return jsonify({"message": "Cập nhật hóa đơn thành công"})

# Xóa hóa đơn
@bp.route("/<ma>", methods=["DELETE"])
def delete_hoa_don(ma):
    hd = HoaDon.query.get(ma)
    if not hd:
        return jsonify({"error": "Không tìm thấy hóa đơn"}), 404

    db.session.delete(hd)
    db.session.commit()
    return jsonify({"message": "Xóa hóa đơn thành công"})
