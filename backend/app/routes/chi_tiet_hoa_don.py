from flask import Blueprint, request, jsonify
from app.models import ChiTietHoaDon
from app import db

bp = Blueprint("chi_tiet_hoa_don", __name__)

# Lấy tất cả chi tiết hóa đơn
@bp.route("/", methods=["GET"])
def get_all_chi_tiet_hoa_don():
    # Lấy danh sách ID nếu có
    ids = request.args.get("ids", default=None, type=str)

    # Nếu có tham số ids, bỏ qua phân trang
    if ids:
        id_list = ids.split(",")
        query = ChiTietHoaDon.query.filter(ChiTietHoaDon.MaHoaDon.in_(id_list))

        # Sắp xếp đúng theo thứ tự truyền vào nếu cần
        items = query.all()

        result = []
        for cthd in items:
            result.append({
                "MaHoaDon": cthd.MaHoaDon,
                "MaNongSan": cthd.MaNongSan,
                "SoLuong": cthd.SoLuong,
                "DonGia": float(cthd.DonGia) if cthd.DonGia else None,
                "GiamGia": float(cthd.GiamGia) if cthd.GiamGia else None
            })

        return jsonify({
            "items": result
        })

    # Trường hợp không có ids: xử lý phân trang
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    query = ChiTietHoaDon.query.order_by(ChiTietHoaDon.MaHoaDon)
    total = query.count()
    ds_cthd = query.offset((page - 1) * limit).limit(limit).all()

    result = []
    for cthd in ds_cthd:
        result.append({
            "MaHoaDon": cthd.MaHoaDon,
            "MaNongSan": cthd.MaNongSan,
            "SoLuong": cthd.SoLuong,
            "DonGia": float(cthd.DonGia) if cthd.DonGia else None,
            "GiamGia": float(cthd.GiamGia) if cthd.GiamGia else None
        })

    return jsonify({
        "items": result,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit,
            "has_next": page * limit < total,
            "has_prev": page > 1
        }
    })


# Lấy chi tiết theo mã hóa đơn và mã nông sản
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
    try:
        cthd = ChiTietHoaDon(
            MaHoaDon=data.get("MaHoaDon"),
            MaNongSan=data.get("MaNongSan"),
            SoLuong=data.get("SoLuong"),
            DonGia=data.get("DonGia"),
            GiamGia=data.get("GiamGia")
        )
        db.session.add(cthd)
        db.session.commit()
        return jsonify({"message": "Tạo chi tiết hóa đơn thành công"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Cập nhật chi tiết hóa đơn
@bp.route("/<ma_hoa_don>/<ma_nong_san>", methods=["PUT"])
def update_chi_tiet_hoa_don(ma_hoa_don, ma_nong_san):
    cthd = ChiTietHoaDon.query.get((ma_hoa_don, ma_nong_san))
    if not cthd:
        return jsonify({"error": "Không tìm thấy chi tiết hóa đơn"}), 404

    data = request.get_json()
    try:
        cthd.SoLuong = data.get("SoLuong")
        cthd.DonGia = data.get("DonGia")
        cthd.GiamGia = data.get("GiamGia")
        db.session.commit()
        return jsonify({
            "message": "Cập nhật chi tiết hóa đơn thành công",
            "ChiTietHoaDon": {
                "MaHoaDon": cthd.MaHoaDon,
                "MaNongSan": cthd.MaNongSan,
                "SoLuong": cthd.SoLuong,
                "DonGia": float(cthd.DonGia),
                "GiamGia": float(cthd.GiamGia) if cthd.GiamGia else 0
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Xóa chi tiết hóa đơn
@bp.route("/<ma_hoa_don>/<ma_nong_san>", methods=["DELETE"])
def delete_chi_tiet_hoa_don(ma_hoa_don, ma_nong_san):
    cthd = ChiTietHoaDon.query.get((ma_hoa_don, ma_nong_san))
    if not cthd:
        return jsonify({"error": "Không tìm thấy chi tiết hóa đơn"}), 404

    try:
        db.session.delete(cthd)
        db.session.commit()
        return jsonify({"message": "Xóa chi tiết hóa đơn thành công"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
