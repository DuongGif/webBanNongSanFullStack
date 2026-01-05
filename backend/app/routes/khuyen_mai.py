from flask import Blueprint, request, jsonify
from app import db
from app.models import KhuyenMai, NongSan
from flask_cors import cross_origin
bp = Blueprint("khuyen_mai", __name__)

# Lấy tất cả khuyến mãi
@bp.route("/", methods=["GET"])
def get_all_khuyenmai():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    query = KhuyenMai.query.order_by(KhuyenMai.MaKhuyenMai)
    total = query.count()
    khuyenmais = query.offset((page - 1) * limit).limit(limit).all()

    result = []
    for km in khuyenmais:
        result.append({
            "MaKhuyenMai": km.MaKhuyenMai,
            "MaNongSan": km.MaNongSan,
            "MoTa": km.MoTa,
            "NgayBatDau": km.NgayBatDau.strftime("%Y-%m-%d") if km.NgayBatDau else None,
            "NgayKetThuc": km.NgayKetThuc.strftime("%Y-%m-%d") if km.NgayKetThuc else None
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

# Lấy khuyến mãi theo mã
@bp.route("/<ma>", methods=["GET"])
def get_by_id(ma):
    km = KhuyenMai.query.get(ma)
    if km:
        return jsonify({
            "MaKhuyenMai": km.MaKhuyenMai,
            "MaNongSan": km.MaNongSan,
            "MoTa": km.MoTa,
            "NgayBatDau": km.NgayBatDau.strftime("%Y-%m-%d") if km.NgayBatDau else None,
            "NgayKetThuc": km.NgayKetThuc.strftime("%Y-%m-%d") if km.NgayKetThuc else None
        })
    return jsonify({"error": "Không tìm thấy"}), 404

# Tạo mới khuyến mãi
@bp.route("", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    ma_khuyen_mai = data.get("MaKhuyenMai")
    ma_nong_san = data.get("MaNongSan")

    # Kiểm tra nếu mã khuyến mãi đã tồn tại
    if KhuyenMai.query.filter_by(MaKhuyenMai=ma_khuyen_mai).first():
        return jsonify({"error": f"Mã khuyến mãi '{ma_khuyen_mai}' đã tồn tại"}), 400

    # Kiểm tra nếu mã nông sản không tồn tại trong bảng NongSan
    if not NongSan.query.filter_by(MaNongSan=ma_nong_san).first():
        return jsonify({"error": f"Mã nông sản '{ma_nong_san}' không tồn tại trong bảng nông sản"}), 400

    km = KhuyenMai(
        MaKhuyenMai=ma_khuyen_mai,
        MaNongSan=ma_nong_san,
        MoTa=data.get("MoTa"),
        NgayBatDau=data.get("NgayBatDau"),
        NgayKetThuc=data.get("NgayKetThuc")
    )

    try:
        db.session.add(km)
        db.session.commit()
        return jsonify({"message": "Tạo khuyến mãi thành công"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Lỗi khi tạo khuyến mãi", "details": str(e)}), 500

# Cập nhật khuyến mãi
@bp.route("/<ma>", methods=["PUT"])
def update(ma):
    km = KhuyenMai.query.get(ma)
    if not km:
        return jsonify({"error": "Không tìm thấy"}), 404
    data = request.get_json()
    km.MaNongSan = data.get("MaNongSan", km.MaNongSan)
    km.MoTa = data.get("MoTa", km.MoTa)
    km.NgayBatDau = data.get("NgayBatDau", km.NgayBatDau)
    km.NgayKetThuc = data.get("NgayKetThuc", km.NgayKetThuc)
    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})

# Xóa khuyến mãi
@bp.route("/<ma>", methods=["DELETE"])
def delete(ma):
    km = KhuyenMai.query.get(ma)
    if not km:
        return jsonify({"error": "Không tìm thấy"}), 404
    db.session.delete(km)
    db.session.commit()
    return jsonify({"message": "Xóa thành công"})
