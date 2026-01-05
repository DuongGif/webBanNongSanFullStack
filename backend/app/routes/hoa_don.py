from flask import Blueprint, request, jsonify
from app.models import HoaDon, ChiTietHoaDon, NongSan
from app import db
from datetime import datetime

bp = Blueprint("hoa_don", __name__)

# Lấy danh sách hóa đơn theo mã tài khoản (mã tài khoản là chuỗi)
@bp.route("/<string:ma_tai_khoan>", methods=["GET"])
def get_hoa_don_by_tai_khoan(ma_tai_khoan):
    hoa_dons = HoaDon.query.filter_by(MaTaiKhoan=ma_tai_khoan).all()
    result = []
    for hd in hoa_dons:
        chi_tiet_list = ChiTietHoaDon.query.filter_by(MaHoaDon=hd.MaHoaDon).all()
        chi_tiet_data = []
        for ct in chi_tiet_list:
            nong_san = NongSan.query.get(ct.MaNongSan)
            chi_tiet_data.append({
                "MaNongSan": ct.MaNongSan,
                "TenNongSan": nong_san.TenNongSan if nong_san else "N/A",
                "SoLuong": ct.SoLuong,
                "DonGia": float(ct.DonGia),
                "GiamGia": float(ct.GiamGia) if ct.GiamGia else 0
            })

        result.append({
            "MaHoaDon": hd.MaHoaDon,
            "NgayXuat": hd.NgayXuat.strftime("%Y-%m-%d") if hd.NgayXuat else None,
            "TongTien": float(hd.TongTien),
            "ChiTiet": chi_tiet_data
        })

    return jsonify(result)

# Lấy danh sách tất cả hóa đơn
@bp.route("/", methods=["GET"])
def get_all_hoa_don():
    # Lấy thông tin phân trang từ query params
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    # Tạo truy vấn cơ bản với mệnh đề ORDER BY
    query = HoaDon.query.order_by(HoaDon.NgayXuat.desc())  # Sắp xếp theo NgayXuat giảm dần

    # Tổng số bản ghi
    total = query.count()

    # Lấy dữ liệu phân trang
    hoa_dons = query.offset((page - 1) * limit).limit(limit).all()

    # Chuẩn bị dữ liệu trả về
    result = [
        {
            "MaHoaDon": hd.MaHoaDon,
            "MaTaiKhoan": hd.MaTaiKhoan,
            "NgayXuat": hd.NgayXuat.strftime("%Y-%m-%d") if hd.NgayXuat else None,
            "TongTien": float(hd.TongTien) if hd.TongTien else None
        } for hd in hoa_dons
    ]

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


# Lấy hóa đơn theo mã
@bp.route("/<string:ma>", methods=["GET"])
def get_hoa_don_by_id(ma):
    hd = HoaDon.query.get(ma)
    if hd:
        return jsonify({
            "MaHoaDon": hd.MaHoaDon,
            "MaTaiKhoan": hd.MaTaiKhoan,
            "NgayXuat": hd.NgayXuat.strftime("%Y-%m-%d") if hd.NgayXuat else None,
            "TongTien": float(hd.TongTien) if hd.TongTien else None
        })
    return jsonify({"error": f"Không tìm thấy hóa đơn với mã số: {ma}"}), 404

# Thêm hóa đơn mới
@bp.route("/", methods=["POST"])
def create_hoa_don():
    data = request.get_json()
    try:
        hd = HoaDon(
            MaHoaDon=data.get("MaHoaDon"),
            MaTaiKhoan=data.get("MaTaiKhoan"),
            NgayXuat=datetime.strptime(data.get("NgayXuat"), "%Y-%m-%d"),
            TongTien=data.get("TongTien")
        )
        db.session.add(hd)
        db.session.commit()
        return jsonify({"message": "Tạo hóa đơn thành công"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Cập nhật hóa đơn
@bp.route("/<string:ma>", methods=["PUT"])
def update_hoa_don(ma):
    hd = HoaDon.query.get(ma)
    if not hd:
        return jsonify({"error": f"Không tìm thấy hóa đơn với mã số: {ma}"}), 404

    data = request.get_json()
    try:
        hd.MaTaiKhoan = data.get("MaTaiKhoan")
        hd.NgayXuat = datetime.strptime(data.get("NgayXuat"), "%Y-%m-%d")
        hd.TongTien = data.get("TongTien")
        db.session.commit()
        return jsonify({
            "message": "Cập nhật hóa đơn thành công",
            "HoaDon": {
                "MaHoaDon": hd.MaHoaDon,
                "MaTaiKhoan": hd.MaTaiKhoan,
                "NgayXuat": hd.NgayXuat.strftime("%Y-%m-%d"),
                "TongTien": float(hd.TongTien)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Xóa hóa đơn
@bp.route("/<ma>", methods=["DELETE"])
def delete_hoa_don(ma):
    hd = HoaDon.query.get(ma)
    if not hd:
        return jsonify({"error": f"Không tìm thấy hóa đơn với mã số: {ma}"}), 404

    try:
        # Xóa chi tiết hóa đơn trước
        ChiTietHoaDon.query.filter_by(MaHoaDon=ma).delete()
        db.session.delete(hd)
        db.session.commit()
        return jsonify({"message": "Xóa hóa đơn thành công"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
